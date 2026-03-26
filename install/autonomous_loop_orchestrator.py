"""
AUTONOMOUS LOOP ORCHESTRATOR — bounded sandbox loop runner

Purpose:
- run the real sandbox loop in this order:

    snapshot -> next_action -> execute -> reconcile -> snapshot

- keep the green controlled test surface as the execution health gate
- write a single stable runtime report
- avoid repo-wide drift and avoid old competing workflow logic
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

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "cmd": cmd,
        }
    except Exception as exc:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(exc),
            "cmd": cmd,
        }


def run_python_file(path: str, args: List[str] | None = None) -> Dict[str, Any]:
    args = args or []
    cmd = [sys.executable, path, *args]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "cmd": cmd,
        }
    except Exception as exc:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(exc),
            "cmd": cmd,
        }


def capture_snapshot(output_path: str) -> Dict[str, Any]:
    script_path = os.path.join(ROOT, "install", "engine", "repo_snapshot.py")
    result = run_python_file(script_path)

    snapshot = load_json(REPO_SNAPSHOT_REPORT, {})
    if not isinstance(snapshot, dict):
        snapshot = {}

    write_json(output_path, snapshot)

    return {
        "ok": result["ok"] and bool(snapshot),
        "runner": result,
        "snapshot": snapshot,
        "output_path": output_path,
    }


def classify_state(pre: Dict[str, Any], post: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(pre, dict) or not isinstance(post, dict):
        return {
            "type": "invalid_snapshot",
            "severity": "critical",
            "action": "halt",
        }

    if pre == post:
        return {
            "type": "no_change",
            "severity": "none",
            "action": "noop",
        }

    signals: List[str] = []

    if pre.get("repo_hash") != post.get("repo_hash"):
        signals.append("repo_modified")

    if pre.get("incoming_bundle_count") != post.get("incoming_bundle_count"):
        signals.append("incoming_bundle_queue_changed")

    if pre.get("installed_bundle_count") != post.get("installed_bundle_count"):
        signals.append("installed_bundle_set_changed")

    if pre.get("failed_bundle_count") != post.get("failed_bundle_count"):
        signals.append("failed_bundle_set_changed")

    if pre.get("last_review_state") != post.get("last_review_state"):
        signals.append("review_state_changed")

    if pre.get("last_next_action") != post.get("last_next_action"):
        signals.append("next_action_changed")

    if pre.get("last_execution_status") != post.get("last_execution_status"):
        signals.append("execution_status_changed")

    if not signals:
        return {
            "type": "opaque_change",
            "severity": "medium",
            "action": "inspect",
            "signals": [],
        }

    if "repo_modified" in signals:
        return {
            "type": "repo_mutation",
            "severity": "high",
            "action": "inspect",
            "signals": signals,
        }

    return {
        "type": "system_activity",
        "severity": "low",
        "action": "observe",
        "signals": signals,
    }


def decide_action(classification: Dict[str, Any]) -> str:
    return classification.get("action", "noop")


def main() -> None:
    started = time.time()

    ensure_dir(PAYLOAD_RUNTIME)
    ensure_dir(BRAIN_REPORTS)

    # 1) health gate first: keep bounded green baseline alive
    ensure_pytest()
    test_result = run_green_tests()

    # 2) snapshot before loop action
    pre = capture_snapshot(PRE_SNAPSHOT_PATH)

    # 3) next_action
    next_action_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "next_action_engine.py")
    )
    next_action_doc = load_json(NEXT_ACTION_REPORT, {})

    # 4) execute
    execute_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "execute_next_action.py")
    )
    execution_doc = load_json(EXECUTION_REPORT, {})

    # 5) reconcile
    reconcile_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "reconcile_execution_state.py")
    )
    reconciled_doc = load_json(RECONCILED_REPORT, {})

    # 6) snapshot after loop action
    post = capture_snapshot(POST_SNAPSHOT_PATH)

    pre_snapshot = pre.get("snapshot", {})
    post_snapshot = post.get("snapshot", {})

    state_changed = isinstance(pre_snapshot, dict) and isinstance(post_snapshot, dict) and pre_snapshot != post_snapshot
    classification = classify_state(pre_snapshot, post_snapshot)
    action = decide_action(classification)

    loop_ok = (
        test_result.get("ok", False)
        and pre.get("ok", False)
        and next_action_runner.get("ok", False)
        and execute_runner.get("ok", False)
        and reconcile_runner.get("ok", False)
        and post.get("ok", False)
    )

    finished = time.time()

    report = {
        "status": "ok",
        "mode": "bounded_sandbox_loop",
        "loop_ok": loop_ok,
        "tests_passed": test_result.get("ok", False),
        "state_changed": state_changed,
        "classification": classification,
        "action": action,
        "duration_seconds": round(finished - started, 3),
        "timestamp": finished,
        "test_surface": GREEN_TEST_SET,
        "test_count": len(GREEN_TEST_SET),
        "pytest_returncode": test_result.get("returncode"),
        "test_output_snippet": extract_summary(
            test_result.get("stdout", ""),
            test_result.get("stderr", ""),
        ),
        "state": {
            "pre": PRE_SNAPSHOT_PATH,
            "post": POST_SNAPSHOT_PATH,
        },
        "artifacts": {
            "repo_snapshot": REPO_SNAPSHOT_REPORT,
            "next_action": NEXT_ACTION_REPORT,
            "execution_result": EXECUTION_REPORT,
            "reconciled_state": RECONCILED_REPORT,
            "runtime_report": REPORT_PATH,
        },
        "steps": {
            "pre_snapshot": {
                "ok": pre.get("ok", False),
                "summary": {
                    "repo_hash": pre_snapshot.get("repo_hash"),
                    "incoming_bundle_count": pre_snapshot.get("incoming_bundle_count"),
                    "installed_bundle_count": pre_snapshot.get("installed_bundle_count"),
                    "failed_bundle_count": pre_snapshot.get("failed_bundle_count"),
                },
                "runner_returncode": (pre.get("runner") or {}).get("returncode"),
            },
            "next_action": {
                "ok": next_action_runner.get("ok", False),
                "runner_returncode": next_action_runner.get("returncode"),
                "summary": next_action_doc.get("next_action", {}),
                "output_snippet": extract_summary(
                    next_action_runner.get("stdout", ""),
                    next_action_runner.get("stderr", ""),
                ),
            },
            "execute": {
                "ok": execute_runner.get("ok", False),
                "runner_returncode": execute_runner.get("returncode"),
                "summary": execution_doc.get("execution", {}),
                "output_snippet": extract_summary(
                    execute_runner.get("stdout", ""),
                    execute_runner.get("stderr", ""),
                ),
            },
            "reconcile": {
                "ok": reconcile_runner.get("ok", False),
                "runner_returncode": reconcile_runner.get("returncode"),
                "summary": reconciled_doc.get("review", {}),
                "output_snippet": extract_summary(
                    reconcile_runner.get("stdout", ""),
                    reconcile_runner.get("stderr", ""),
                ),
            },
            "post_snapshot": {
                "ok": post.get("ok", False),
                "summary": {
                    "repo_hash": post_snapshot.get("repo_hash"),
                    "incoming_bundle_count": post_snapshot.get("incoming_bundle_count"),
                    "installed_bundle_count": post_snapshot.get("installed_bundle_count"),
                    "failed_bundle_count": post_snapshot.get("failed_bundle_count"),
                },
                "runner_returncode": (post.get("runner") or {}).get("returncode"),
            },
        },
    }

    write_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
