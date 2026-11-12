"""Semantic invariants for the shared synthetic frontend fixture.

Run from the repository root:
    python -m unittest discover -s poc/frontend/shared/tests -v

These tests complement (but do not replace) JSON Schema Draft 2020-12 validation.
"""
from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "research-demo.json"
SCHEMA_PATH = ROOT / "schemas" / "research-demo.schema.json"

EXPECTED_SCENARIOS = {
    "overview",
    "research-valid",
    "research-invalid-range",
    "partial-data",
    "not-available",
    "recoverable-error",
    "evaluation-comparison",
}


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"Timestamp must include timezone: {value}")
    return parsed.astimezone(timezone.utc)


class SharedFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_both_documents_are_valid_json(self) -> None:
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_fixture_is_explicitly_synthetic(self) -> None:
        self.assertEqual(self.fixture["disclosure"], "DEMO — DATOS SINTÉTICOS")
        self.assertEqual(self.fixture["environmentStatus"], "SIMULATED")
        self.assertEqual(self.fixture["researchResult"]["status"], "SIMULATED")
        self.assertEqual(self.fixture["researchResult"]["uncertainty"]["status"], "NOT_QUANTIFIED")

    def test_required_scenario_set_is_exact_and_unique(self) -> None:
        scenarios = self.fixture["scenarios"]
        identifiers = [scenario["id"] for scenario in scenarios]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(set(identifiers), EXPECTED_SCENARIOS)

    def test_invalid_range_scenario_is_chronologically_invalid(self) -> None:
        scenario = next(item for item in self.fixture["scenarios"] if item["id"] == "research-invalid-range")
        self.assertGreater(
            parse_timestamp(scenario["input"]["start"]),
            parse_timestamp(scenario["input"]["end"]),
        )
        self.assertEqual(scenario["expectedState"], "VALIDATION_ERROR")

    def test_missing_interval_is_inside_selected_period(self) -> None:
        period = self.fixture["researchSelection"]["period"]
        start = parse_timestamp(period["start"])
        end = parse_timestamp(period["end"])
        self.assertLessEqual(start, end)
        for interval in self.fixture["dataQuality"]["coverage"]["missingIntervals"]:
            missing_start = parse_timestamp(interval["start"])
            missing_end = parse_timestamp(interval["end"])
            self.assertLessEqual(start, missing_start)
            self.assertLessEqual(missing_start, missing_end)
            self.assertLessEqual(missing_end, end)

    def test_evaluation_references_are_unique_and_synthetic(self) -> None:
        evaluations = self.fixture["evaluations"]
        ids = [item["id"] for item in evaluations]
        self.assertGreaterEqual(len(evaluations), 2)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(item["status"] == "SIMULATED" for item in evaluations))
        comparison = next(item for item in self.fixture["scenarios"] if item["id"] == "evaluation-comparison")
        self.assertEqual(set(comparison["evaluationIds"]), set(ids))

    def test_not_available_and_partial_states_are_not_promoted(self) -> None:
        self.assertEqual(self.fixture["dataQuality"]["status"], "PARTIAL")
        states = {item["id"]: item["status"] for item in self.fixture["researchResult"]["sections"]}
        self.assertEqual(states["technical-structure"], "NOT_AVAILABLE")

    def test_fixture_contains_no_market_series(self) -> None:
        forbidden = {"open", "high", "low", "close", "volume", "price", "return", "probability"}
        def walk(value):
            if isinstance(value, dict):
                for key, nested in value.items():
                    yield key.lower()
                    yield from walk(nested)
            elif isinstance(value, list):
                for nested in value:
                    yield from walk(nested)
        self.assertTrue(forbidden.isdisjoint(set(walk(self.fixture))))


if __name__ == "__main__":
    unittest.main()
