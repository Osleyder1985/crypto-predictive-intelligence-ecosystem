# Shared frontend POC fixtures

**Status:** experimental test input; not a production domain contract or API.
**Purpose:** make the Next.js, React SPA, React Native + Expo, and Flutter POCs exercise equivalent content and states.

## Rules

1. Consume the same `fixtures/research-demo.json` in every implementation. Do not fork or hand-edit per-framework copies.
2. Validate the fixture against `schemas/research-demo.schema.json` before rendering it.
3. Preserve the persistent `DEMO — DATOS SINTÉTICOS` disclosure on every screen, including history and comparison.
4. The BTC symbol is a navigation/demo identifier only. All identifiers, timestamps, event descriptions, evidence, and evaluation records in this fixture are synthetic. No market prices, returns, probabilities, signals, or causal claims are supplied.
5. A UI may format or arrange fixture fields, but must not invent missing values, convert missing data into zero, or upgrade a status.
6. A demo “save” operation must remain local and explicitly say “no persistido”. Reloading may reset it; do not imply server persistence.
7. Keep domain decisions out of the clients. These fixtures are a temporary adapter input and must later be replaced by a versioned API contract without changing domain semantics.

## Required scenarios

The `scenarios` array defines framework-neutral observable outcomes:

- `overview`: show demo banner and the two synthetic history entries.
- `research-valid`: accept the valid BTC demo selection and display SIMULATED content.
- `research-invalid-range`: reject an end date earlier than the start date; expose a field-level validation message.
- `partial-data`: show PARTIAL and its explicit coverage limitation; never imply completeness.
- `not-available`: show NOT_AVAILABLE for a capability with no fixture evidence.
- `recoverable-error`: show ERROR and a retry affordance; do not relabel it as empty data.
- `evaluation-comparison`: compare the two synthetic records by their metadata; do not claim market improvement or deterioration.

## Comparison protocol

Each POC must record pass/fail and evidence for the same scenarios, viewport/device, and interaction sequence. Record toolchain versions, clean-install/build commands, build result, test result, accessibility observations, artifact size, and resource measurements separately. Do not compare a web browser build with a mobile emulator run as if they were the same workload.

No performance thresholds or framework weights are defined here. They must come from approved requirements before scoring.

## Scope boundary

This is fixture data and a manual/automated test contract only. It is not a backend, OpenAPI definition, authentication mechanism, persistence layer, real market dataset, or proof of production readiness.
