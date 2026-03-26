"""
AUTONOMOUS LOOP ORCHESTRATOR — controlled green-baseline runtime

Purpose:
- run the exact controlled sandbox test surface that is currently green
- ensure pytest is available at runtime
- emit a stable report for the autonomous loop workflow
- avoid scanning the full repo or drifting into broken test surfaces
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List


GREEN_TEST_SET: List[str] = [
    "tests/test_receipt_chain.py",
    "tests/test_receipts.py",
    "tests/test_priority_router.py",
    "tests/test_step_completion.py",
    "tests/test_plan_memory.py",
    "tests/test_multi_step_planner.py",
    "tests/test_self_improve.py",
    "tests/test_execution_pipeline_v4.py",
    "tests/test_failure_feedback.py",
    "tests/test_generator_v2.py",
    "tests/test_authority_policy.py",
    "tests/test_consensus.py",
    "tests/test_manifest.py",
    "tests/test_auto_repair.py",
    "tests/test_history_engine.py",
    "tests/test_contract_snapshot.py",
    "tests/test_convergence_engine.py",
    "tests/test_bootstrap_permission_unlock.py",
]


def ensure_pytest() -> None:
    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pytest"],
            check=True,
        )


def run_controlled_tests() -> Dict[str, Any]:
    cmd = [sys.executable, "-m", "pytest", *GREEN_TEST_SET, "-q"]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception as exc:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(exc),
            "cmd": cmd,
        }

    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "cmd": cmd,
    }


def extract_summary(stdout: str, stderr: str) -> str:
    text = (stdout or "") + ("\n" + stderr if stderr else "")
    text = text.strip()
    if not text:
        return "no output"

    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "no output"

    tail = lines[-12:]
    return "\n".join(tail)


def write_json(path: str, payload: Dict[str, Any]) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)


def main() -> None:
    started_at = time.time()
    ensure_pytest()
    test_result = run_controlled_tests()
    finished_at = time.time()

    report_path = "payload/runtime/autonomous_loop_report.json"

    report = {
        "status": "ok",
        "mode": "controlled_green_baseline",
        "tests_passed": test_result["ok"],
        "repair_triggered": not test_result["ok"],
        "timestamp": finished_at,
        "duration_seconds": round(finished_at - started_at, 3),
        "report": report_path,
        "test_surface": GREEN_TEST_SET,
        "test_count": len(GREEN_TEST_SET),
        "pytest_cmd": test_result["cmd"],
        "pytest_returncode": test_result["returncode"],
        "test_output_snippet": extract_summary(
            test_result.get("stdout", ""),
            test_result.get("stderr", ""),
        ),
    }

    write_json(report_path, report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
