# Python CPIE quantitative workload POC

## Purpose

Validate a bounded CPU-only quantitative data/model workflow on Python 3.12.x for the Windows 11 development target. This is the next stage after package installation/import smoke tests; it exercises interoperability and small model training/inference.

## What the probe does

- Generates deterministic **synthetic** market-like OHLCV data using a fixed seed. It is not historical BTC data and cannot establish market predictability.
- Builds lagged returns, rolling volatility and volume features. The target is the sign of the next bar return.
- Uses a chronological 80/20 train/test split and purges one boundary row because its t+1 label would otherwise touch the test period. The scaler is fitted only on the training partition.
- Runs a causality mutation test: it changes all raw close/volume values from a future cutoff onward and asserts that earlier feature rows remain unchanged.
- Builds the same features in pandas and Polars and asserts numeric/target parity.
- Converts pandas data through a PyArrow table and verifies round-trip schema shape.
- Trains/infer small CPU baselines with scikit-learn LogisticRegression, XGBoost, LightGBM and a small PyTorch MLP.
- Limits major CPU thread pools and tree-model workers to two. The default workload is 12,000 source rows; accepted range is 1,000–50,000.
- Records package versions, stage/model durations, CPU time, available RAM before/after and sampled peak process RSS in a JSON report.

## Preconditions

Use the already-created isolated Python 3.12 virtual environment with the dependencies installed by the compatibility POC. This script does not install or upgrade packages. Do not run another package installation, Docker-heavy workload or second benchmark concurrently.

From the repository root in PowerShell:

~~~powershell
.\.venv-poc-312\Scripts\Activate.ps1
python --version
python .\scripts\poc\python_cpi_workload_probe.py --output .\poc-results\python-cpi-workload-3.12.json
~~~

The script rejects Python versions outside 3.12.x and row counts outside the documented range. To repeat with identical input, use the same seed (default 20261110) and row count.

## Report interpretation

- PASS means all four model training/inference paths completed, predictions were finite and within [0,1], tabular parity checks passed, the causal-feature mutation test passed, and the chronological split with boundary purge passed.
- Model accuracy/log-loss are **technical smoke outputs on synthetic data only**. They are not evidence of alpha, BTC predictability, profitability, or model quality.
- Timings are local observations, not pass/fail thresholds and not comparable across machines without controlled conditions.
- Peak RSS is sampled every 100 ms and may miss shorter spikes; it is not the OS absolute peak.
- Available system RAM is measured before and after the workload. This does not isolate the process's total memory contribution.
- The probe does not test GPU/CUDA, concurrent workloads, PostgreSQL, API, production datasets, exchange connectivity or trading.

## Acceptance evidence

Attach the JSON report to Issue #83 and reference it from Issue #5. Review errors, versions, resource observations and limitations before any baseline decision. A passing workload POC is necessary evidence, not sufficient approval of the complete technology stack.
