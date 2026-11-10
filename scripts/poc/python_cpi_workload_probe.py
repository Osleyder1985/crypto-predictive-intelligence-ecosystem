from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import threading
import time
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

# Keep CPU parallelism bounded on the 16 GB Windows development machine.
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "2")

import lightgbm as lgb
import numpy as np
import pandas as pd
import polars as pl
import psutil
import pyarrow as pa
import torch
import torch.nn as nn
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

FEATURES = ["ret_1", "ret_5", "vol_20", "volume_z20"]
SEED_DEFAULT = 20261110
SAMPLE_INTERVAL_SECONDS = 0.1


class PeakRssSampler:
    def __init__(self, process: psutil.Process) -> None:
        self.process = process
        self.stop_event = threading.Event()
        self.peak_rss = 0
        self.thread = threading.Thread(target=self._sample, daemon=True)

    def _sample(self) -> None:
        while not self.stop_event.is_set():
            try:
                self.peak_rss = max(self.peak_rss, self.process.memory_info().rss)
            except psutil.Error:
                pass
            self.stop_event.wait(SAMPLE_INTERVAL_SECONDS)

    def __enter__(self) -> "PeakRssSampler":
        self.thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop_event.set()
        self.thread.join(timeout=2)


def package_versions() -> dict[str, str | None]:
    distributions = [
        "numpy", "pandas", "polars", "pyarrow", "scikit-learn",
        "xgboost", "lightgbm", "torch", "psutil", "threadpoolctl",
    ]
    result: dict[str, str | None] = {}
    for distribution in distributions:
        try:
            result[distribution] = version(distribution)
        except PackageNotFoundError:
            result[distribution] = None
    return result


def build_synthetic_market_data(rows: int, seed: int) -> tuple[pd.DataFrame, pl.DataFrame]:
    rng = np.random.default_rng(seed)
    log_returns = 0.0001 + rng.normal(0.0, 0.008, rows)
    close = 50_000.0 * np.exp(np.cumsum(log_returns))
    volume = rng.lognormal(mean=7.0, sigma=0.35, size=rows)

    raw = {
        "bar_index": np.arange(rows, dtype=np.int64),
        "close": close.astype(np.float64),
        "volume": volume.astype(np.float64),
    }
    pandas_frame = pd.DataFrame(raw)
    polars_frame = pl.DataFrame(raw)

    pandas_frame["ret_1"] = pandas_frame["close"].pct_change()
    pandas_frame["ret_5"] = pandas_frame["close"].pct_change(5)
    pandas_frame["vol_20"] = pandas_frame["ret_1"].rolling(20, min_periods=20).std()
    volume_mean = pandas_frame["volume"].rolling(20, min_periods=20).mean()
    volume_std = pandas_frame["volume"].rolling(20, min_periods=20).std()
    pandas_frame["volume_z20"] = (pandas_frame["volume"] - volume_mean) / volume_std
    future_return = pandas_frame["ret_1"].shift(-1)
    pandas_frame["target"] = (future_return > 0).astype("float64")
    pandas_frame.loc[future_return.isna(), "target"] = np.nan
    pandas_frame = pandas_frame.dropna(subset=FEATURES + ["target"]).reset_index(drop=True)

    polars_frame = polars_frame.with_columns(
        pl.col("close").pct_change().alias("ret_1")
    ).with_columns(
        [
            pl.col("close").pct_change(5).alias("ret_5"),
            pl.col("ret_1").rolling_std(window_size=20).alias("vol_20"),
            (
                (pl.col("volume") - pl.col("volume").rolling_mean(window_size=20))
                / pl.col("volume").rolling_std(window_size=20)
            ).alias("volume_z20"),
            (pl.col("ret_1").shift(-1) > 0).cast(pl.Int8).alias("target"),
        ]
    ).drop_nulls(subset=FEATURES + ["target"])

    return pandas_frame, polars_frame


def assert_tabular_interoperability(
    pandas_frame: pd.DataFrame, polars_frame: pl.DataFrame
) -> dict[str, object]:
    pandas_values = pandas_frame[FEATURES].to_numpy(dtype=np.float64)
    polars_values = polars_frame.select(FEATURES).to_numpy()
    np.testing.assert_allclose(pandas_values, polars_values, rtol=1e-7, atol=1e-10)

    pandas_target = pandas_frame["target"].to_numpy(dtype=np.int8)
    polars_target = polars_frame["target"].to_numpy().astype(np.int8)
    np.testing.assert_array_equal(pandas_target, polars_target)

    arrow_table = pa.Table.from_pandas(pandas_frame, preserve_index=False)
    arrow_roundtrip = arrow_table.to_pandas()
    if list(arrow_roundtrip.columns) != list(pandas_frame.columns):
        raise AssertionError("PyArrow round-trip changed the column order")
    if arrow_roundtrip.shape != pandas_frame.shape:
        raise AssertionError("PyArrow round-trip changed the frame shape")

    return {
        "rows": int(len(pandas_frame)),
        "feature_count": len(FEATURES),
        "pandas_polars_feature_values_equal": True,
        "pandas_polars_targets_equal": True,
        "pyarrow_roundtrip_shape_equal": True,
        "arrow_table_bytes": int(arrow_table.nbytes),
    }



def assert_feature_causality(pandas_frame: pd.DataFrame) -> dict[str, object]:
    # Perturb all raw observations from a future cutoff onward. Features strictly
    # before that cutoff must remain unchanged, proving the feature transform is causal.
    raw = pandas_frame[["bar_index", "close", "volume"]].copy()
    cutoff = int(raw["bar_index"].iloc[len(raw) // 2])
    future_mask = raw["bar_index"] >= cutoff
    future_count = int(future_mask.sum())
    altered = raw.copy()
    altered.loc[future_mask, "close"] *= np.exp(
        np.linspace(0.05, 0.25, future_count, dtype=np.float64)
    )
    altered.loc[future_mask, "volume"] *= 1.75

    altered["ret_1"] = altered["close"].pct_change()
    altered["ret_5"] = altered["close"].pct_change(5)
    altered["vol_20"] = altered["ret_1"].rolling(20, min_periods=20).std()
    volume_mean = altered["volume"].rolling(20, min_periods=20).mean()
    volume_std = altered["volume"].rolling(20, min_periods=20).std()
    altered["volume_z20"] = (altered["volume"] - volume_mean) / volume_std

    # Start after the truncated raw frame's rolling warm-up period.
    compare_mask = (raw["bar_index"] >= 40) & (raw["bar_index"] < cutoff)
    expected = pandas_frame.loc[compare_mask, FEATURES].to_numpy(dtype=np.float64)
    observed = altered.loc[compare_mask, FEATURES].to_numpy(dtype=np.float64)
    np.testing.assert_allclose(expected, observed, rtol=1e-7, atol=1e-10)
    return {
        "status": "PASS",
        "mutation_starts_at_bar_index": cutoff,
        "unchanged_feature_rows_compared": int(compare_mask.sum()),
        "future_raw_values_mutated": True,
    }

def evaluate_probabilities(y_true: np.ndarray, probabilities: np.ndarray) -> dict[str, float]:
    probabilities = np.asarray(probabilities, dtype=np.float64).reshape(-1)
    if len(probabilities) != len(y_true):
        raise AssertionError("Prediction count differs from test target count")
    if not np.isfinite(probabilities).all():
        raise AssertionError("Model returned non-finite probabilities")
    if ((probabilities < 0.0) | (probabilities > 1.0)).any():
        raise AssertionError("Model probabilities fall outside [0, 1]")
    predictions = (probabilities >= 0.5).astype(np.int8)
    return {
        "accuracy": float(accuracy_score(y_true, predictions)),
        "log_loss": float(log_loss(y_true, probabilities, labels=[0, 1])),
        "test_rows": int(len(y_true)),
    }


def train_and_evaluate(
    X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray,
    seed: int,
) -> dict[str, object]:
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train).astype(np.float32)
    X_test_scaled = scaler.transform(X_test).astype(np.float32)
    results: dict[str, object] = {}

    models = [
        (
            "sklearn_logistic_regression",
            LogisticRegression(max_iter=250, random_state=seed),
            X_train_scaled,
            X_test_scaled,
        ),
        (
            "xgboost_cpu",
            xgb.XGBClassifier(
                n_estimators=40, max_depth=3, learning_rate=0.05,
                subsample=0.9, colsample_bytree=0.9, n_jobs=2,
                random_state=seed, eval_metric="logloss", verbosity=0,
            ),
            X_train,
            X_test,
        ),
        (
            "lightgbm_cpu",
            lgb.LGBMClassifier(
                n_estimators=40, max_depth=3, num_leaves=7,
                learning_rate=0.05, n_jobs=2, random_state=seed, verbosity=-1,
            ),
            X_train,
            X_test,
        ),
    ]

    for name, model, train_features, test_features in models:
        started = time.perf_counter()
        model.fit(train_features, y_train)
        fit_seconds = time.perf_counter() - started
        started = time.perf_counter()
        probabilities = model.predict_proba(test_features)[:, 1]
        predict_seconds = time.perf_counter() - started
        results[name] = {
            **evaluate_probabilities(y_test, probabilities),
            "fit_seconds": round(fit_seconds, 6),
            "predict_seconds": round(predict_seconds, 6),
            "status": "PASS",
        }

    torch.manual_seed(seed)
    torch.set_num_threads(2)
    train_tensor = torch.from_numpy(X_train_scaled)
    target_tensor = torch.from_numpy(y_train.astype(np.float32))
    test_tensor = torch.from_numpy(X_test_scaled)

    class SmallMlp(nn.Module):
        def __init__(self, input_features: int) -> None:
            super().__init__()
            self.layers = nn.Sequential(
                nn.Linear(input_features, 16),
                nn.ReLU(),
                nn.Linear(16, 8),
                nn.ReLU(),
                nn.Linear(8, 1),
            )

        def forward(self, values: torch.Tensor) -> torch.Tensor:
            return self.layers(values).squeeze(1)

    model = SmallMlp(X_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_function = nn.BCEWithLogitsLoss()
    started = time.perf_counter()
    model.train()
    for _ in range(6):
        for start in range(0, len(train_tensor), 256):
            end = start + 256
            optimizer.zero_grad(set_to_none=True)
            logits = model(train_tensor[start:end])
            loss = loss_function(logits, target_tensor[start:end])
            loss.backward()
            optimizer.step()
    fit_seconds = time.perf_counter() - started

    started = time.perf_counter()
    model.eval()
    with torch.no_grad():
        probabilities = torch.sigmoid(model(test_tensor)).cpu().numpy()
    predict_seconds = time.perf_counter() - started
    results["pytorch_mlp_cpu"] = {
        **evaluate_probabilities(y_test, probabilities),
        "fit_seconds": round(fit_seconds, 6),
        "predict_seconds": round(predict_seconds, 6),
        "status": "PASS",
        "device": "cpu",
        "epochs": 6,
        "torch_threads": torch.get_num_threads(),
    }
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bounded synthetic CPIE-style CPU workload; not a market-prediction benchmark."
    )
    parser.add_argument("--rows", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=SEED_DEFAULT)
    parser.add_argument("--output", default="poc-results/python-cpi-workload-3.12.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {
        "schema_version": 1,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "seed": args.seed,
        "requested_rows": args.rows,
        "feature_columns": FEATURES,
        "thread_limits": {
            "OMP_NUM_THREADS": os.environ["OMP_NUM_THREADS"],
            "MKL_NUM_THREADS": os.environ["MKL_NUM_THREADS"],
            "OPENBLAS_NUM_THREADS": os.environ["OPENBLAS_NUM_THREADS"],
            "NUMEXPR_NUM_THREADS": os.environ["NUMEXPR_NUM_THREADS"],
            "torch_threads": 2,
            "tree_model_jobs": 2,
        },
        "package_versions": package_versions(),
        "stages": {},
        "models": {},
    }

    if sys.version_info[:2] != (3, 12):
        report["result"] = "INVALID_RUNTIME"
        report["error"] = "This workload POC is scoped to Python 3.12.x."
        output.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"result": report["result"], "report": str(output)}, indent=2))
        return 2
    if not 1000 <= args.rows <= 50000:
        report["result"] = "INVALID_ROWS"
        report["error"] = "--rows must be between 1000 and 50000."
        output.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"result": report["result"], "report": str(output)}, indent=2))
        return 2

    process = psutil.Process()
    vm_before = psutil.virtual_memory()
    cpu_before = process.cpu_times()
    started_all = time.perf_counter()

    try:
        with PeakRssSampler(process) as sampler, threadpool_limits(limits=2):
            stage_started = time.perf_counter()
            pandas_frame, polars_frame = build_synthetic_market_data(args.rows, args.seed)
            report["stages"]["synthetic_data_and_features_seconds"] = round(
                time.perf_counter() - stage_started, 6
            )

            stage_started = time.perf_counter()
            report["interoperability"] = assert_tabular_interoperability(
                pandas_frame, polars_frame
            )
            report["stages"]["tabular_interoperability_seconds"] = round(
                time.perf_counter() - stage_started, 6
            )

            # The split is chronological. Features at t use data through t;
            # the label is the sign of the return at t+1.
            X = pandas_frame[FEATURES].to_numpy(dtype=np.float32)
            y = pandas_frame["target"].to_numpy(dtype=np.int8)
            timestamps = pandas_frame["bar_index"].to_numpy(dtype=np.int64)
            split = int(len(X) * 0.8)
            train_stop = split - 1  # Purge the boundary row: its t+1 label would touch the test period.
            if train_stop <= 0 or split >= len(X):
                raise AssertionError("Chronological train/test split is empty")
            train_last = int(timestamps[:train_stop].max())
            test_first = int(timestamps[split:].min())
            if train_last + 1 >= test_first:
                raise AssertionError("Train/test boundary was not purged")
            if X.shape[0] != y.shape[0] or not np.isfinite(X).all():
                raise AssertionError("Feature matrix is invalid")
            causality = assert_feature_causality(pandas_frame)
            report["temporal_validation"] = {
                "status": "PASS",
                "split": "chronological 80/20 with one boundary row purged",
                "train_last_bar_index": train_last,
                "test_first_bar_index": test_first,
                "purged_boundary_rows": 1,
                "target_definition": "sign of next bar return (t+1)",
                "feature_causality_mutation_test": causality,
                "scaler_fit_on_training_partition_only": True,
            }

            stage_started = time.perf_counter()
            report["models"] = train_and_evaluate(
                X[:train_stop], y[:train_stop], X[split:], y[split:], args.seed
            )
            report["stages"]["model_training_and_inference_seconds"] = round(
                time.perf_counter() - stage_started, 6
            )
            report["peak_process_rss_bytes_sampled"] = int(sampler.peak_rss)
    except Exception as exc:
        report["result"] = "FAIL"
        report["error"] = repr(exc)

    report["total_workload_seconds"] = round(time.perf_counter() - started_all, 6)
    cpu_after = process.cpu_times()
    vm_after = psutil.virtual_memory()
    report["resources"] = {
        "logical_cpu_count": psutil.cpu_count(logical=True),
        "physical_cpu_count": psutil.cpu_count(logical=False),
        "total_memory_bytes": vm_before.total,
        "available_memory_bytes_before": vm_before.available,
        "available_memory_bytes_after": vm_after.available,
        "process_cpu_seconds": round(
            (cpu_after.user + cpu_after.system) - (cpu_before.user + cpu_before.system), 6
        ),
        "peak_rss_sampling_interval_seconds": SAMPLE_INTERVAL_SECONDS,
        "peak_rss_is_sampled_not_os_absolute_peak": True,
    }
    if "result" not in report:
        report["result"] = (
            "PASS" if len(report["models"]) == 4
            and all(model.get("status") == "PASS" for model in report["models"].values())
            else "FAIL"
        )
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "result": report["result"],
        "python": report["python"],
        "rows": args.rows,
        "models": list(report["models"]),
        "total_workload_seconds": report["total_workload_seconds"],
        "report": str(output),
    }, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
