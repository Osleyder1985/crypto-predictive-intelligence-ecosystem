# Python Windows compatibility POC

## Purpose

Compare two isolated Windows x64 environments without prematurely selecting a project-wide Python baseline:

- Python 3.15: general scientific/data stack candidate.
- Python 3.12: compatibility lane that additionally probes the official PyTorch CPU wheel channel.

This workflow runs on a GitHub-hosted Windows runner. It is a package-availability and smoke-test experiment, **not** a performance benchmark of the developer's Windows 11 computer.

## Execution

The workflow runs on relevant pull requests and can also be started manually through GitHub Actions.

Each matrix job:
1. Installs the requested Python minor line using actions/setup-python.
2. Records the exact interpreter and machine metadata.
3. Installs packages independently using binary wheels only. A missing wheel is recorded as a compatibility failure rather than silently compiling source.
4. Imports each package and records the exact imported version.
5. Runs deterministic NumPy, SciPy, pandas, Polars and PyArrow smoke tests.
6. On Python 3.12 only, installs PyTorch from its official CPU wheel index and runs a CPU tensor operation.
7. Uploads a JSON evidence artifact even when a matrix job fails.

The initial probe covers NumPy, SciPy, pandas, Polars, PyArrow, scikit-learn, statsmodels, XGBoost, LightGBM, Pydantic, FastAPI, psutil and (on the compatibility lane) PyTorch.

This discovery POC intentionally does not pin dependency versions. The report records the exact versions resolved at execution time. A later validated baseline must pin exact versions and hashes in lockfiles.

## Important interpretation

- A green GitHub Actions job proves only that the recorded installation/import/smoke checks passed on that hosted runner at that time.
- It does not prove compatibility with all CPIE workloads, native drivers, local hardware, memory constraints or production conditions.
- A failed install is evidence to inspect, not an automatic reason to abandon a technology. Review the captured log and determine whether the blocker is a missing wheel, unsupported interpreter, transient index failure or package defect.
- GitHub-hosted runner RAM and CPU are not representative of the target 16 GB Windows 11 computer.
- Do not use these results to approve PyTorch GPU/CUDA, trading execution or a production baseline.

## Local execution on Windows 11

Prerequisite: install Python 3.15 x64 and Python 3.12 x64 side-by-side. Use the Python launcher if available; otherwise call each interpreter by its full executable path. Do not change the global PATH or uninstall an existing runtime merely for this POC.

Run the script separately in each interpreter:

~~~powershell
py -3.15 scripts/poc/python_stack_probe.py --output poc-results/python-stack-local-3.15.json
py -3.12 scripts/poc/python_stack_probe.py --with-pytorch --output poc-results/python-stack-local-3.12.json
~~~

If the py launcher is unavailable, invoke the exact python.exe path for each installed runtime. For strict isolation, create a separate virtual environment per runtime before running the script. The script installs packages into the interpreter environment selected for that invocation.

For a meaningful local resource profile, record:
- Windows edition/build, CPU model, logical/physical cores and architecture.
- Installed RAM and available RAM before the run.
- Per-package installation time, total run time, peak memory if measured with a suitable external monitor, and disk growth.
- Whether other applications or Docker services were running.

Do not run both package-installation lanes concurrently on a 16 GB machine.

## Evidence and acceptance

Store generated JSON reports as workflow artifacts and attach local reports to the corresponding Issue/PR evidence. Review every failure and compare exact resolved package versions before deciding on a compatibility lane.

This POC does not close Issue #5 and does not create a Validated Baseline. Approval requires reviewed results, reproducible lockfiles, integration tests, security/license review and a separate resource/performance evaluation on the target hardware.
