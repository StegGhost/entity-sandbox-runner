import os
import json
import time
import subprocess
from pathlib import Path

ROOT = Path(os.getcwd())

BRAIN_REPORTS = ROOT / "brain_reports"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
OUTPUT_PATH = BRAIN_REPORTS / "execution_result.json"

FAILED_DIR = ROOT / "failed_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"

REPAIRED_DIR.mkdir(parents=True, exist_ok=True)


def now_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def load_next_action():
    if not NEXT_ACTION_PATH.exists():
        return None
    return json.loads(NEXT_ACTION_PATH.read_text())


def run_repair(target_path: str):
    target = Path(target_path)

    if not target.exists():
        return {
            "status": "failed",
            "reason": "target_not_found",
            "target": target_path
        }

    output_bundle = REPAIRED_DIR / target.name

    try:
        # Call your repair engine
        result = subprocess.run(
            ["python", "install/engine/repair_bundle_engine.py", str(target)],
            capture_output=True,
            text=True
        )

        return {
            "status": "ok" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "input_bundle": str(target),
            "output_bundle": str(output_bundle)
        }

    except Exception as e:
        return {
            "status": "failed",
            "reason": "exception",
            "error": str(e)
        }


def run_inspect(target_path: str):
    target = Path(target_path)

    if not target.exists():
        return {
            "status": "failed",
            "reason": "target_not_found",
            "target": target_path
        }

    try:
        result = subprocess.run(
            ["python", "install/engine/preflight_gate.py", str(target)],
            capture_output=True,
            text=True
        )

        return {
            "status": "ok" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "target": str(target)
        }

    except Exception as e:
        return {
            "status": "failed",
            "reason": "exception",
            "error": str(e)
        }


def main():
    action = load_next_action()

    if not action:
        result = {
            "status": "failed",
            "reason": "missing_next_action"
        }
    elif action.get("status") == "idle":
        result = {
            "status": "idle",
            "reason": "no_work"
        }
    else:
        target = action.get("target")

        if not target:
            result = {
                "status": "failed",
                "reason": "missing_target"
            }
        else:
            action_type = action.get("action")

            if action_type == "repair_bundle":
                worker = run_repair(target)
            elif action_type == "inspect_bundle":
                worker = run_inspect(target)
            else:
                worker = {
                    "status": "failed",
                    "reason": "unknown_action",
                    "action": action_type
                }

            result = {
                "status": worker.get("status"),
                "ts": now_ts(),
                "action": action_type,
                "target": target,
                "worker_result": worker
            }

    OUTPUT_PATH.write_text(json.dumps(result, indent=2))

    print(json.dumps({
        "status": result["status"],
        "output": str(OUTPUT_PATH),
        "result": result
    }, indent=2))


if __name__ == "__main__":
    main()
