"""
AUTONOMOUS LOOP ORCHESTRATOR — controlled green-baseline runtime + state diff

Adds:
- pre/post snapshot capture
- deterministic state diff detection
- loop_ok invariant (true health signal)
"""

from __future__ import annotations

import importlib
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
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[-12:]) if lines else "no output"


def write_json(path: str, payload: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)


def _capture_snapshot(output_path: str) -> Dict[str, Any]:
    try:
        module = importlib.import_module("install.engine.repo_snapshot")
    except Exception as exc:
        payload = {"ok": False, "error": str(exc)}
        write_json(output_path, payload)
        return payload

    try:
        if hasattr(module, "write_snapshot"):
            snapshot = module.write_snapshot(output_path=output_path)
        elif hasattr(module, "build_snapshot"):
            snapshot = module.build_snapshot()
            write_json(output_path, snapshot)
        else:
            raise RuntimeError("snapshot api missing")

        return {"ok": True, "snapshot": snapshot}

    except Exception as exc:
        payload = {"ok": False, "error": str(exc)}
        write_json(output_path, payload)
        return payload


def main() -> None:
    started = time.time()

    pre_path = "payload/runtime/system_snapshot_pre.json"
    post_path = "payload/runtime/system_snapshot_post.json"
    report_path = "payload/runtime/autonomous_loop_report.json"

    # 🔥 capture state BEFORE execution
    pre = _capture_snapshot(pre_path)

    ensure_pytest()
    test_result = run_controlled_tests()

    # 🔥 capture state AFTER execution
    post = _capture_snapshot(post_path)

    finished = time.time()

    # 🔥 state diff (simple but deterministic)
    state_changed = False
    if pre.get("ok") and post.get("ok"):
        state_changed = pre["snapshot"] != post["snapshot"]

    # 🔥 real loop health invariant
    loop_ok = (
        test_result["ok"]
        and pre.get("ok")
        and post.get("ok")
    )

    report = {
        "status": "ok",
        "mode": "controlled_green_baseline",
        "loop_ok": loop_ok,
        "tests_passed": test_result["ok"],
        "repair_triggered": not test_result["ok"],
        "state_changed": state_changed,
        "timestamp": finished,
        "duration_seconds": round(finished - started, 3),
        "report": report_path,
        "test_count": len(GREEN_TEST_SET),
        "pytest_returncode": test_result["returncode"],
        "test_output_snippet": extract_summary(
            test_result.get("stdout", ""),
            test_result.get("stderr", ""),
        ),
        "state": {
            "pre": pre_path,
            "post": post_path,
        },
    }

    write_json(report_path, report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
