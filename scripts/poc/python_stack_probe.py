from __future__ import annotations

import argparse
import importlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PACKAGES = [
    ("psutil", "psutil"),
    ("numpy", "numpy"), ("scipy", "scipy"), ("pandas", "pandas"),
    ("polars", "polars"), ("pyarrow", "pyarrow"),
    ("scikit-learn", "sklearn"), ("statsmodels", "statsmodels"),
    ("xgboost", "xgboost"), ("lightgbm", "lightgbm"),
    ("pydantic", "pydantic"), ("fastapi", "fastapi"),
]


def run(command: list[str], timeout: int = 600) -> tuple[int, str]:
    completed = subprocess.run(
        command, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    return completed.returncode, completed.stdout[-12000:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-pytorch", action="store_true")
    parser.add_argument("--output", default="poc-results/python-stack-report.json")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    report: dict = {
        "schema_version": 1,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "pytorch_lane": args.with_pytorch,
        "package_results": [],
        "smoke_tests": [],
    }

    try:
        import psutil
        vm = psutil.virtual_memory()
        report["hardware"] = {
            "logical_cpu_count": psutil.cpu_count(logical=True),
            "physical_cpu_count": psutil.cpu_count(logical=False),
            "total_memory_bytes": vm.total,
            "available_memory_bytes_at_start": vm.available,
        }
    except Exception as exc:
        report["hardware_probe_error"] = repr(exc)

    packages = list(PACKAGES)
    if args.with_pytorch:
        packages.append(("torch", "torch"))

    failures = 0
    for distribution, module in packages:
        started = time.perf_counter()
        if distribution == "torch":
            command = [
                sys.executable, "-m", "pip", "install", "--upgrade",
                "--only-binary=:all:", "--index-url",
                "https://download.pytorch.org/whl/cpu", "torch",
            ]
        else:
            command = [
                sys.executable, "-m", "pip", "install", "--upgrade",
                "--only-binary=:all:", distribution,
            ]

        try:
            code, log = run(command)
        except subprocess.TimeoutExpired:
            code, log = 124, "Installation timed out after 600 seconds."
        install_ok = code == 0
        import_ok = False
        import_error = None
        module_version = None

        if install_ok:
            try:
                imported = importlib.import_module(module)
                module_version = getattr(imported, "__version__", None)
                import_ok = True
            except Exception as exc:
                import_error = repr(exc)

        item = {
            "distribution": distribution,
            "module": module,
            "install_ok": install_ok,
            "import_ok": import_ok,
            "module_version": module_version,
            "duration_seconds": round(time.perf_counter() - started, 3),
            "return_code": code,
            "install_log_tail": log,
            "import_error": import_error,
        }
        report["package_results"].append(item)
        if not (install_ok and import_ok):
            failures += 1

    tests = [
        ("numpy_array", lambda: __import__("numpy").array([1, 2, 3]).sum() == 6),
        ("scipy_linear_algebra", lambda: abs(__import__("scipy").linalg.det([[1.0, 2.0], [3.0, 4.0]]) + 2.0) < 1e-9),
        ("pandas_dataframe", lambda: __import__("pandas").DataFrame({"x": [1, 2]}).shape == (2, 1)),
        ("polars_dataframe", lambda: __import__("polars").DataFrame({"x": [1, 2]}).height == 2),
        ("pyarrow_table", lambda: __import__("pyarrow").table({"x": [1, 2]}).num_rows == 2),
    ]
    for name, test in tests:
        try:
            passed, error = bool(test()), None
        except Exception as exc:
            passed, error = False, repr(exc)
        report["smoke_tests"].append({"name": name, "passed": passed, "error": error})
        if not passed:
            failures += 1

    if args.with_pytorch:
        try:
            import torch
            tensor = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
            expected = torch.tensor([[7.0, 10.0], [15.0, 22.0]])
            passed, error = bool(torch.equal(tensor @ tensor, expected)), None
            report["pytorch"] = {
                "version": torch.__version__,
                "cuda_available": torch.cuda.is_available(),
                "device_test": "CPU tensor matrix multiplication",
            }
        except Exception as exc:
            passed, error = False, repr(exc)
        report["smoke_tests"].append({"name": "pytorch_cpu_tensor", "passed": passed, "error": error})
        if not passed:
            failures += 1

    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    report["failure_count"] = failures
    report["result"] = "PASS" if failures == 0 else "FAIL"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "result": report["result"],
        "python": platform.python_version(),
        "architecture": platform.machine(),
        "failure_count": failures,
        "report": str(output),
    }, indent=2))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
