"""
AUTONOMOUS LOOP ORCHESTRATOR — controlled baseline + classification

Adds:
- state diff
- mutation classification (inline, no new files)
- loop invariant enforcement
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


# 🔥 INLINE CLASSIFIER (no extra files)
def classify_state(pre: Dict[str, Any], post: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(pre, dict) or not isinstance(post, dict):
        return {"type": "invalid", "severity": "critical", "action": "halt"}

    if pre == post:
        return {"type": "no_change", "severity": "none", "action": "noop"}

    if pre.get("repo_hash") != post.get("repo_hash"):
        return {
            "type": "repo_mutation",
            "severity": "high",
            "action": "inspect",
        }

    return {
        "type": "system_activity",
        "severity": "low",
        "action": "observe",
    }


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


def run_tests() -> Dict[str, Any]:
    cmd = [sys.executable, "-m", "pytest", *GREEN_TEST_SET, "-q"]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

    return {
        "ok": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def extract_summary(stdout: str, stderr: str) -> str:
    text = (stdout or "") + ("\n" + stderr if stderr else "")
    lines = [l for l in text.splitlines() if l.strip()]
    return "\n".join(lines[-10:]) if lines else "no output"


def write_json(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def snapshot(path: str) -> Dict[str, Any]:
    try:
        mod = importlib.import_module("install.engine.repo_snapshot")

        if hasattr(mod, "write_snapshot"):
            snap = mod.write_snapshot(output_path=path)
        else:
            snap = mod.build_snapshot()
            write_json(path, snap)

        return snap if isinstance(snap, dict) else {"value": snap}

    except Exception as e:
        data = {"error": str(e)}
        write_json(path, data)
        return data


def main() -> None:
    start = time.time()

    pre_path = "payload/runtime/system_snapshot_pre.json"
    post_path = "payload/runtime/system_snapshot_post.json"
    report_path = "payload/runtime/autonomous_loop_report.json"

    pre = snapshot(pre_path)

    ensure_pytest()
    test = run_tests()

    post = snapshot(post_path)

    changed = pre != post
    classification = classify_state(pre, post)

    loop_ok = (
        test.get("ok")
        and isinstance(pre, dict)
        and isinstance(post, dict)
    )

    report = {
        "status": "ok",
        "loop_ok": loop_ok,
        "tests_passed": test.get("ok"),
        "state_changed": changed,
        "classification": classification,
        "duration": round(time.time() - start, 3),
        "summary": extract_summary(test.get("stdout", ""), test.get("stderr", "")),
        "state": {
            "pre": pre_path,
            "post": post_path,
        },
    }

    write_json(report_path, report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
