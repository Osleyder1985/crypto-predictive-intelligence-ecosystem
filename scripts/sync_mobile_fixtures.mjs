import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceDir = path.join(root, "poc/frontend/shared");
const targets = [
  "poc/mobile/react-native/assets/fixtures",
  "poc/mobile/flutter/assets/fixtures",
];
const files = ["research-demo.json", "research-demo.schema.json"];
const checkOnly = process.argv.includes("--check");
const digest = (value) => createHash("sha256").update(value).digest("hex");

for (const target of targets) {
  const destination = path.join(root, target);
  if (!checkOnly) await mkdir(destination, { recursive: true });
  for (const name of files) {
    const source = await readFile(path.join(sourceDir, name));
    const targetPath = path.join(destination, name);
    if (checkOnly) {
      const actual = await readFile(targetPath);
      if (digest(actual) !== digest(source)) {
        throw new Error(`Fixture hash mismatch: ${target}/${name}`);
      }
    } else {
      await copyFile(path.join(sourceDir, name), targetPath);
      const copied = await readFile(targetPath);
      if (digest(copied) !== digest(source)) {
        throw new Error(`Fixture copy verification failed: ${target}/${name}`);
      }
    }
    console.log(`${checkOnly ? "PASS" : "SYNC"} ${target}/${name} sha256=${digest(source)}`);
  }
}

const fixture = JSON.parse(await readFile(path.join(sourceDir, files[0]), "utf8"));
const scenarioIds = fixture.scenarios.map((scenario) => scenario.id);
const expected = [
  "overview",
  "research-valid",
  "research-invalid-range",
  "partial-data",
  "not-available",
  "recoverable-error",
  "evaluation-comparison",
];
if (JSON.stringify(scenarioIds) !== JSON.stringify(expected)) {
  throw new Error("Shared fixture scenario set/order changed; review the mobile POC contract.");
}
console.log("PASS canonical fixture parses and contains the expected seven scenarios.");
