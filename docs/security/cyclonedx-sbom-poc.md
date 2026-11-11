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

This establishes repeatability of this specific local generation, not completeness of discovery or a production supply-chain control. The generated JSON files remain in the local worktree's `poc-results/` directory; their contents have not yet been committed or retained as CI artifacts. The generated tooling lockfile exists locally as an untracked file and still requires diff/review and commit.

## Preliminary SBOM inventory inspection

The maintainer's PowerShell inspection confirmed:

- 42 package components are present in the generated SBOM.
- All 42 report at least one declared license entry according to the CycloneDX `licenses` field; no component was returned by the query for an empty license array.
- The SBOM metadata identifies the root application as `cpie-python-supply-chain-poc` version `0.1.0`.
- The metadata timestamp is `1970-01-01T00:00:00+00:00`, expected from the explicitly fixed `SOURCE_DATE_EPOCH=0` used to make output reproducible. This is not the actual generation time and must not be interpreted as such.
- The displayed component inventory includes the quantitative workload packages (including NumPy, pandas, Polars, PyArrow, scikit-learn, SciPy, XGBoost, LightGBM and PyTorch CPU) and their visible Python dependencies.

This is only a structural inventory check. A non-empty declared license field does not establish license correctness, compatibility, completeness, or legal clearance. Exact SPDX identifiers/expressions and dependency-edge coverage still require inspection. The maintainer's first license report grouped 15 components as MIT, 12 as BSD-3-Clause, 4 as Apache-2.0, and the remaining 11 across BSD-2-Clause, PSF-2.0, composite SPDX expressions and legacy license-classifier text. Five components (Jinja2, mpmath, patsy, SciPy and SymPy) expose the legacy text `License :: OSI Approved :: BSD License`; this is not a precise SPDX identifier and must not be silently normalized to a specific BSD variant. NumPy and PyTorch expose composite SPDX expressions, which need separate review. The corrected graph inspection found 43 known BOM references (42 package components plus the metadata root), 43 graph nodes, 124 non-null edges, and zero unresolved non-null references. No node reference was null. PowerShell's follow-up inspection established that exactly 15 leaf components omit the optional `dependsOn` property, 28 nodes have dependency arrays, and there are zero explicit null properties, empty arrays, or null array elements. This is consistent with leaf nodes and is not a dangling-reference defect. The subsequent `uv lock --check` completed successfully (34 packages resolved).

### Targeted license-file review — exact pinned versions

The following primary-source files were checked at the exact package release tag (or exact release metadata where noted):

| Component | Version | Evidence | Finding |
|---|---:|---|---|
| Jinja2 | 3.1.6 | [Pallets LICENSE.txt](https://github.com/pallets/jinja/blob/3.1.6/LICENSE.txt) | Three-clause BSD text; normalize to `BSD-3-Clause`. |
| mpmath | 1.3.0 | [mpmath LICENSE](https://github.com/mpmath/mpmath/blob/1.3.0/LICENSE) | Three conditions, including non-endorsement; `BSD-3-Clause`. |
| patsy | 1.0.3 | [Patsy LICENSE.txt](https://github.com/pydata/patsy/blob/v1.0.3/LICENSE.txt) | Main package is `BSD-2-Clause`; `patsy.compat` contains Python standard-library-derived code under `PSF-2.0`. Preserve both obligations in the inventory; do not flatten to one license. |
| SciPy | 1.18.1 | [SciPy LICENSE.txt](https://github.com/scipy/scipy/blob/v1.18.1/LICENSE.txt), [LICENSES_bundled.txt](https://github.com/scipy/scipy/blob/v1.18.1/LICENSES_bundled.txt), [release pyproject.toml](https://github.com/scipy/scipy/blob/v1.18.1/pyproject.toml) | Main project license is BSD-style three-clause. The release also lists bundled components under distinct licenses (including BSD-2-Clause, MIT, BSL-1.0, Qhull and others). The package-level CycloneDX field does not enumerate all bundled notices; wheel-level/native inventory remains required. |
| SymPy | 1.14.0 | [SymPy LICENSE](https://github.com/sympy/sympy/blob/1.14.0/LICENSE) | Main license text is three-clause BSD, and the same file includes third-party portions under BSD terms plus an MIT-licensed latex2sympy portion. The package-level SBOM declaration is therefore incomplete as a notice inventory; retain BSD and MIT notices. |

The evidence supports a practical normalized summary for the top-level distributions, but it does **not** justify claiming a complete third-party notice inventory for SciPy or SymPy. The SBOM's license expression for PyTorch is consistent with the exact release's `pyproject.toml`; that release explicitly lists a large set of third-party license files, so the wheel contents and notices must still be checked. Patsy's embedded PSF-licensed compatibility code also demonstrates why a single legacy classifier is insufficient.

This is a technical metadata review, not legal advice or a legal clearance decision. For redistributions, the actual installed wheel's `*.dist-info/licenses` files and bundled native notices take precedence over a generic PyPI classifier.

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
- [x] Preliminary count and missing-license-field check (42 components; none with an empty license array).
- [x] Inventory license declarations and flag legacy/non-SPDX classifier strings for manual verification.
- [x] Review exact release license files for Jinja2, mpmath, patsy, SciPy and SymPy; record embedded/bundled notices and unresolved package-level metadata limitations.
- [x] Confirm PyTorch's composite SPDX expression against its exact release metadata; bundled wheel notices remain in scope for artifact-level review.
- [x] Validate non-null dependency graph references: 43 nodes, 124 non-null edges, zero unresolved references.
- [x] Confirm the 15 nodes without `dependsOn` are leaf nodes: 28 nodes have dependencies; zero explicit null properties, empty arrays or null array elements.
- [ ] Add CI generation and artifact retention after local command and output are verified.
- [ ] Compare against a separately pinned Syft run.
- [ ] Triage vulnerabilities and license/copyright findings.
