# CycloneDX SBOM generation POC

- Issue: #86
- Branch: `poc/issue-86-cyclonedx-sbom`
- Generator candidate: `cyclonedx-bom==7.6.0`
- Scope: Windows x64, CPython 3.12.10, the locked CPIE Python workload environment.
- Status: local Windows 11 / CPython 3.12.10 execution passed for lock resolution/check, isolated tooling reconstruction, CycloneDX 1.6 schema validation and two identical SBOM generations. Lockfile and generated SBOM evidence still need review/commit or controlled artifact retention; component/license inspection and complementary scans remain pending.

## Why a separate tooling environment

The generator is isolated from the workload environment so that SBOM tooling does not become an application/runtime dependency. Its own `pyproject.toml` and `uv.lock` pin the generator's transitive graph and artifact hashes. This first POC intentionally targets Python 3.12 only; support for running the generator on Python 3.15 is not assumed.

CycloneDX Python does not parse `uv.lock` directly. It inspects the installed target environment, which is reconstructed separately from the workload lock. The SBOM therefore describes the installed environment, not a direct serialization of the lockfile.

## Initial lock creation — one-time maintainer action

Run from the repository root on Windows PowerShell. The command creates the isolated lockfile; review and commit the resulting `poc/supply-chain/sbom/uv.lock` in this branch.

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:TEMP\cpie-sbom-tooling-312"
& $uv lock --project .\poc\supply-chain\sbom
if ($LASTEXITCODE -ne 0) { throw "uv lock failed" }
& $uv lock --check --project .\poc\supply-chain\sbom
if ($LASTEXITCODE -ne 0) { throw "uv lock --check failed" }
```

Do not regenerate the existing workload lock at `poc/supply-chain/python/uv.lock` as part of this step.

## Reconstruct tooling and generate SBOM

This uses the existing clean workload environment `%TEMP%\cpie-uv-312-clean2` as the target. The tooling environment is separate.

```powershell
$env:UV_PROJECT_ENVIRONMENT = "$env:TEMP\cpie-sbom-tooling-312"
& $uv sync --locked --project .\poc\supply-chain\sbom --python 3.12
if ($LASTEXITCODE -ne 0) { throw "SBOM tooling sync failed" }

$targetPython = "$env:TEMP\cpie-uv-312-clean2\Scripts\python.exe"
if (-not (Test-Path $targetPython)) { throw "Target Python environment not found: $targetPython" }

New-Item -ItemType Directory -Force .\poc-results | Out-Null
$env:SOURCE_DATE_EPOCH = "0"

& $uv run --project .\poc\supply-chain\sbom --locked cyclonedx-py environment $targetPython --pyproject .\poc\supply-chain\python\pyproject.toml --output-reproducible --validate --spec-version 1.6 --output-format JSON --output-file .\poc-results\python-312-environment.cdx.json
if ($LASTEXITCODE -ne 0) { throw "CycloneDX generation or validation failed" }

Get-FileHash .\poc-results\python-312-environment.cdx.json -Algorithm SHA256
```

The fixed `SOURCE_DATE_EPOCH=0` is used to remove time-based variability in this POC. It is not the actual build time; record the execution timestamp separately in the evidence report. Re-run generation twice against the unchanged target environment and compare SHA-256 before claiming deterministic output.

## Local execution evidence — Windows 11

Execution completed in an isolated Git worktree at commit `73ad6febd77c1de82eb74be3682230c7f5c748cb`.

- `uv lock`: passed; resolver reported 34 packages.
- `uv lock --check`: passed.
- `uv sync --locked`: passed; isolated generator environment installed 33 packages, including `cyclonedx-bom==7.6.0`.
- Target interpreter: CPython 3.12.10 at `%TEMP%\\cpie-uv-312-clean2\\Scripts\\python.exe`.
- CycloneDX generation with `--output-reproducible --validate --spec-version 1.6 --output-format JSON`: both runs passed.
- Output: CycloneDX format, specification 1.6, 42 components, 43 dependency entries.
- SHA-256, both generated files: `9D26064913D909AF5B7E602B3212FBD617255733E164A26436B54A9C2A2A70C6`.
- Result: byte-for-byte reproducibility demonstrated for these two runs against the unchanged target environment.

This establishes repeatability of this specific local generation, not completeness of discovery or a production supply-chain control. The generated JSON files remain in the local worktree's `poc-results/` directory; their contents have not yet been committed or retained as CI artifacts. The generated tooling lockfile also still requires a Git diff/review and commit.

## Required inspection before acceptance

1. Confirm CycloneDX schema validation passes.
2. Record SBOM component count, dependency relationships, missing/unknown license fields and metadata.
3. Inspect whether native/runtime components are represented; do not assume Python package inventory covers Windows system libraries or all wheel-bundled native code.
4. Compare component coverage against Syft in a separate, pinned tooling POC.
5. Review declared license metadata against actual LICENSE/NOTICE files and bundled third-party notices. The SBOM license field is not legal clearance.
6. Preserve the generated SBOM and SHA-256 as CI artifacts linked to commit, runtime, OS and generator lock hash. Local reports are not repository evidence until attached/published through the approved workflow.

## Explicit limitations

- Python 3.15 generator compatibility is not tested by this first POC.
- No Syft comparison, vulnerability scan, license-file audit or legal review is included.
- A valid CycloneDX document does not prove completeness of component discovery.
- The SBOM describes the actual installed target environment and may differ from a lock's theoretical resolution if the environment was not freshly reconstructed from that exact lock.
- Do not upload the generated SBOM to a public service without reviewing whether it reveals internal project structure or dependency details.

## Acceptance status

- [x] Isolated generator manifest created with exact top-level version.
- [x] Generate a transitive `uv.lock` and pass `uv lock --check` (review/commit the resulting file still pending).
- [x] Reconstruct the isolated generator environment with `uv sync --locked`.
- [x] Generate a CycloneDX 1.6 SBOM with schema validation from the Python 3.12 target environment.
- [x] Repeat generation twice and obtain identical SHA-256 hashes.
- [ ] Inspect component graph, licenses and detection gaps.
- [ ] Add CI generation and artifact retention after local command and output are verified.
- [ ] Compare against a separately pinned Syft run.
- [ ] Triage vulnerabilities and license/copyright findings.
