"""
AUTONOMOUS LOOP ORCHESTRATOR — bounded sandbox loop runner (with observer integration)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List


ROOT = os.getcwd()
PAYLOAD_RUNTIME = os.path.join(ROOT, "payload", "runtime")
BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")

REPORT_PATH = os.path.join(PAYLOAD_RUNTIME, "autonomous_loop_report.json")
PRE_SNAPSHOT_PATH = os.path.join(PAYLOAD_RUNTIME, "system_snapshot_pre.json")
POST_SNAPSHOT_PATH = os.path.join(PAYLOAD_RUNTIME, "system_snapshot_post.json")

REPO_SNAPSHOT_REPORT = os.path.join(BRAIN_REPORTS, "repo_snapshot.json")
EXPLORE_REPORT = os.path.join(BRAIN_REPORTS, "explore.json")
NEXT_ACTION_REPORT = os.path.join(BRAIN_REPORTS, "next_action.json")
EXECUTION_REPORT = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")
RECONCILED_REPORT = os.path.join(BRAIN_REPORTS, "reconciled_state.json")


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


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_json(path: str, payload: Dict[str, Any]) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


def load_json(path: str, default: Any = None) -> Any:
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def extract_summary(stdout: str, stderr: str, tail_lines: int = 12) -> str:
    text = (stdout or "") + ("\n" + stderr if stderr else "")
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "no output"
    return "\n".join(lines[-tail_lines:])


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


def run_green_tests() -> Dict[str, Any]:
    cmd = [sys.executable, "-m", "pytest", *GREEN_TEST_SET, "-q"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def run_python_file(path: str) -> Dict[str, Any]:
    result = subprocess.run(
        [sys.executable, path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def capture_snapshot(output_path: str) -> Dict[str, Any]:
    script_path = os.path.join(ROOT, "install", "engine", "repo_snapshot.py")
    runner = run_python_file(script_path)
    snapshot = load_json(REPO_SNAPSHOT_REPORT, {})
    write_json(output_path, snapshot)
    return {"ok": runner["ok"], "snapshot": snapshot}


def main() -> None:
    started = time.time()

    ensure_dir(PAYLOAD_RUNTIME)
    ensure_dir(BRAIN_REPORTS)

    ensure_pytest()
    test_result = run_green_tests()

    # 1. Snapshot (state)
    pre = capture_snapshot(PRE_SNAPSHOT_PATH)

    # 2. Activity observer
    explore_runner = run_python_file(
        os.path.join(ROOT, "internal_brain", "explore.py")
    )
    explore_doc = load_json(EXPLORE_REPORT, {})

    # 3. Decision
    next_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "next_action_engine.py")
    )
    next_doc = load_json(NEXT_ACTION_REPORT, {})

    # 4. Execute
    exec_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "execute_next_action.py")
    )
    exec_doc = load_json(EXECUTION_REPORT, {})

    # 5. Reconcile
    recon_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "reconcile_execution_state.py")
    )
    recon_doc = load_json(RECONCILED_REPORT, {})

    # 6. Snapshot again
    post = capture_snapshot(POST_SNAPSHOT_PATH)

    finished = time.time()

    report = {
        "status": "ok",
        "mode": "sandbox_loop_with_observer",
        "loop_ok": test_result["ok"],
        "duration_seconds": round(finished - started, 3),
        "tests_passed": test_result["ok"],
        "activity": explore_doc.get("counts", {}),
        "next_action": next_doc.get("next_action", {}),
        "execution": exec_doc.get("execution", {}),
        "reconcile": recon_doc.get("review", {}),
        "state": {
            "pre": PRE_SNAPSHOT_PATH,
            "post": POST_SNAPSHOT_PATH,
        }
    }

    write_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
