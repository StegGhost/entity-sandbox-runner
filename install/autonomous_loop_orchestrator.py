"""
AUTONOMOUS LOOP ORCHESTRATOR — repo-state aware bounded sandbox loop runner

Purpose:
- run the real sandbox loop in this order:

    system_state -> snapshot -> explore -> next_action -> execute -> reconcile -> snapshot

- keep the green controlled test surface as the execution health gate
- write a single stable runtime report
- read authoritative system state from payload/context/SYSTEM_STATE_v2.md when present
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
CONTEXT_DIR = os.path.join(ROOT, "payload", "context")

REPORT_PATH = os.path.join(PAYLOAD_RUNTIME, "autonomous_loop_report.json")
PRE_SNAPSHOT_PATH = os.path.join(PAYLOAD_RUNTIME, "system_snapshot_pre.json")
POST_SNAPSHOT_PATH = os.path.join(PAYLOAD_RUNTIME, "system_snapshot_post.json")

SYSTEM_STATE_V2_PATH = os.path.join(CONTEXT_DIR, "SYSTEM_STATE_v2.md")
SYSTEM_STATE_V1_PATH = os.path.join(CONTEXT_DIR, "SYSTEM_STATE_v1.md")

REPO_SNAPSHOT_REPORT = os.path.join(BRAIN_REPORTS, "repo_snapshot.json")
EXPLORE_REPORT = os.path.join(BRAIN_REPORTS, "explore.json")
NEXT_ACTION_REPORT = os.path.join(BRAIN_REPORTS, "next_action.json")
EXECUTION_REPORT = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")
RECONCILED_REPORT = os.path.join(BRAIN_REPORTS, "reconciled_state.json")
INTERNAL_BRAIN_REPORT = os.path.join(ROOT, "internal_brain", "brain_report.json")


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


def load_text(path: str, default: str = "") -> str:
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return default


def resolve_system_state() -> Dict[str, Any]:
    if os.path.exists(SYSTEM_STATE_V2_PATH):
        text = load_text(SYSTEM_STATE_V2_PATH, "")
        return {
            "path": SYSTEM_STATE_V2_PATH,
            "version": "v2",
            "present": bool(text.strip()),
            "text": text,
        }

    text = load_text(SYSTEM_STATE_V1_PATH, "")
    return {
        "path": SYSTEM_STATE_V1_PATH,
        "version": "v1",
        "present": bool(text.strip()),
        "text": text,
    }


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
        "cmd": cmd,
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
        "cmd": [sys.executable, path],
    }


def capture_snapshot(output_path: str) -> Dict[str, Any]:
    script_path = os.path.join(ROOT, "install", "engine", "repo_snapshot.py")
    runner = run_python_file(script_path)
    snapshot = load_json(REPO_SNAPSHOT_REPORT, {})
    snapshot = snapshot if isinstance(snapshot, dict) else {}
    write_json(output_path, snapshot)
    return {
        "ok": runner["ok"] and bool(snapshot),
        "runner": runner,
        "snapshot": snapshot,
        "output_path": output_path,
    }


def build_activity_summary(explore_doc: Dict[str, Any], next_doc: Dict[str, Any], internal_brain_doc: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(explore_doc, dict) and explore_doc.get("counts"):
        return {
            "source": "explore_json",
            "counts": explore_doc.get("counts", {}),
            "summary": explore_doc.get("summary"),
            "mode": explore_doc.get("mode"),
        }

    next_action = next_doc.get("next_action", {}) if isinstance(next_doc, dict) else {}
    if next_action.get("source") == "internal_brain":
        return {
            "source": "next_action_internal_brain",
            "counts": {},
            "summary": next_action.get("reason"),
            "mode": "internal_brain_signal",
            "active_family": next_action.get("active_family"),
            "target": next_action.get("target"),
        }

    closure = internal_brain_doc.get("closure_output", {}) if isinstance(internal_brain_doc, dict) else {}
    actions = closure.get("actions", []) if isinstance(closure, dict) else []
    if actions:
        first = actions[0]
        return {
            "source": "internal_brain_report",
            "counts": {},
            "summary": first.get("reason"),
            "mode": "internal_brain_signal",
            "action": first.get("action"),
            "priority": first.get("priority"),
            "targets": first.get("targets", []),
        }

    return {
        "source": "none",
        "counts": {},
        "summary": "no observer activity surfaced",
        "mode": "missing",
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
    if pre.get("has_work") != post.get("has_work"):
        signals.append("work_presence_changed")
    if pre.get("cge_state") != post.get("cge_state"):
        signals.append("cge_state_changed")

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


def main() -> None:
    started = time.time()

    ensure_dir(PAYLOAD_RUNTIME)
    ensure_dir(BRAIN_REPORTS)
    ensure_dir(CONTEXT_DIR)

    system_state = resolve_system_state()

    ensure_pytest()
    test_result = run_green_tests()

    pre = capture_snapshot(PRE_SNAPSHOT_PATH)

    explore_runner = run_python_file(
        os.path.join(ROOT, "internal_brain", "explore.py")
    )
    explore_doc = load_json(EXPLORE_REPORT, {})

    next_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "next_action_engine.py")
    )
    next_doc = load_json(NEXT_ACTION_REPORT, {})

    exec_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "execute_next_action.py")
    )
    exec_doc = load_json(EXECUTION_REPORT, {})

    recon_runner = run_python_file(
        os.path.join(ROOT, "install", "engine", "reconcile_execution_state.py")
    )
    recon_doc = load_json(RECONCILED_REPORT, {})

    post = capture_snapshot(POST_SNAPSHOT_PATH)

    internal_brain_doc = load_json(INTERNAL_BRAIN_REPORT, {})
    activity = build_activity_summary(explore_doc, next_doc, internal_brain_doc)

    pre_snapshot = pre.get("snapshot", {})
    post_snapshot = post.get("snapshot", {})
    classification = classify_state(pre_snapshot, post_snapshot)
    state_changed = (
        isinstance(pre_snapshot, dict)
        and isinstance(post_snapshot, dict)
        and pre_snapshot != post_snapshot
    )

    finished = time.time()

    report = {
        "status": "ok",
        "mode": "sandbox_loop_with_observer",
        "loop_ok": (
            test_result["ok"]
            and pre["ok"]
            and next_runner["ok"]
            and exec_runner["ok"]
            and recon_runner["ok"]
            and post["ok"]
        ),
        "duration_seconds": round(finished - started, 3),
        "timestamp": finished,
        "tests_passed": test_result["ok"],
        "pytest_returncode": test_result["returncode"],
        "test_surface": GREEN_TEST_SET,
        "test_count": len(GREEN_TEST_SET),
        "test_output_snippet": extract_summary(
            test_result.get("stdout", ""),
            test_result.get("stderr", ""),
        ),
        "system_state": {
            "path": system_state["path"],
            "version": system_state["version"],
            "present": system_state["present"],
            "bytes": len(system_state["text"].encode("utf-8")) if system_state["text"] else 0,
            "preview": system_state["text"][:400],
        },
        "activity": activity,
        "state_changed": state_changed,
        "classification": classification,
        "next_action": next_doc.get("next_action", {}),
        "execution": exec_doc.get("execution", {}),
        "reconcile": recon_doc.get("review", {}),
        "artifacts": {
            "repo_snapshot": REPO_SNAPSHOT_REPORT,
            "explore": EXPLORE_REPORT,
            "next_action": NEXT_ACTION_REPORT,
            "execution_result": EXECUTION_REPORT,
            "reconciled_state": RECONCILED_REPORT,
            "internal_brain_report": INTERNAL_BRAIN_REPORT,
            "runtime_report": REPORT_PATH,
        },
        "steps": {
            "explore": {
                "ok": explore_runner["ok"],
                "returncode": explore_runner["returncode"],
                "output_snippet": extract_summary(
                    explore_runner.get("stdout", ""),
                    explore_runner.get("stderr", ""),
                ),
                "explore_json_present": bool(explore_doc),
            },
            "next_action": {
                "ok": next_runner["ok"],
                "returncode": next_runner["returncode"],
                "output_snippet": extract_summary(
                    next_runner.get("stdout", ""),
                    next_runner.get("stderr", ""),
                ),
            },
            "execute": {
                "ok": exec_runner["ok"],
                "returncode": exec_runner["returncode"],
                "output_snippet": extract_summary(
                    exec_runner.get("stdout", ""),
                    exec_runner.get("stderr", ""),
                ),
            },
            "reconcile": {
                "ok": recon_runner["ok"],
                "returncode": recon_runner["returncode"],
                "output_snippet": extract_summary(
                    recon_runner.get("stdout", ""),
                    recon_runner.get("stderr", ""),
                ),
            },
        },
        "state": {
            "pre": PRE_SNAPSHOT_PATH,
            "post": POST_SNAPSHOT_PATH,
        },
    }

    write_json(REPORT_PATH, report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
