import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import Ajv2020 from "ajv/dist/2020/index.js";

const fixture = JSON.parse(await readFile(new URL("../assets/fixtures/research-demo.json", import.meta.url), "utf8"));
const schema = JSON.parse(await readFile(new URL("../assets/fixtures/research-demo.schema.json", import.meta.url), "utf8"));

test("shared fixture validates against the Draft 2020-12 schema", () => {
  const ajv = new Ajv2020({ allErrors: true });
  assert.equal(ajv.validate(schema, fixture), true, JSON.stringify(ajv.errors));
});

test("fixture exposes exactly the seven agreed mobile scenarios", () => {
  assert.deepEqual(fixture.scenarios.map((item) => item.id), [
    "overview", "research-valid", "research-invalid-range", "partial-data",
    "not-available", "recoverable-error", "evaluation-comparison",
  ]);
});

test("fixture remains synthetic and does not contain market series values", () => {
  assert.equal(fixture.environmentStatus, "SIMULATED");
  assert.equal(fixture.disclosure, "DEMO — DATOS SINTÉTICOS");
  assert.equal(fixture.dataQuality.status, "PARTIAL");
  assert.equal(fixture.researchResult.uncertainty.status, "NOT_QUANTIFIED");
  assert.equal(fixture.researchResult.sections.find((item) => item.id === "technical-structure").status, "NOT_AVAILABLE");
  assert.equal(fixture.evaluations.length, 2);
  for (const forbidden of ["open", "high", "low", "close", "volume", "price", "probability"]) {
    assert.equal(Object.hasOwn(fixture, forbidden), false);
  }
});
