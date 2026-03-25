import os
import json
import shutil
import subprocess
from datetime import datetime


BRAIN_REPORT_PATH = "internal_brain/brain_report.json"
OUTPUT_PATH = "brain_reports/execute_next_action_result.json"

FAILED_DIR = "failed_bundles"
INCOMING_DIR = "incoming_bundles"


def load_brain_report():
    if not os.path.exists(BRAIN_REPORT_PATH):
        return None
    with open(BRAIN_REPORT_PATH, "r") as f:
        return json.load(f)


def ensure_dirs():
    os.makedirs("brain_reports", exist_ok=True)
    os.makedirs(INCOMING_DIR, exist_ok=True)


# 🔧 ACTION: inspect_failed_bundle_family
def inspect_failed_bundle_family(target):
    if not target or not os.path.exists(target):
        return {
            "status": "failed",
            "executed": False,
            "reason": "target_not_found",
            "target": target
        }

    bundle_name = os.path.basename(target)
    dst = os.path.join(INCOMING_DIR, bundle_name)

    try:
        shutil.move(target, dst)
    except Exception as e:
        return {
            "status": "failed",
            "executed": False,
            "reason": str(e),
            "target": target
        }

    return {
        "status": "ok",
        "executed": True,
        "action": "inspect_failed_bundle_family",
        "moved_to_incoming": dst,
        "bundle": bundle_name,
        "trigger_ingestion": True
    }


def execute_action(action_obj):
    action = action_obj.get("action")
    target = action_obj.get("target")

    if action == "inspect_failed_bundle_family":
        return inspect_failed_bundle_family(target)

    return {
        "status": "failed",
        "executed": False,
        "reason": "unknown_or_unsupported_action",
        "action": action,
        "target": target
    }


def main():
    ensure_dirs()

    brain = load_brain_report()
    if not brain:
        result = {
            "generated_at": datetime.utcnow().isoformat(),
            "error": "brain_report_not_found"
        }
        with open(OUTPUT_PATH, "w") as f:
            json.dump(result, f, indent=2)
        return

    next_action = brain.get("next_action")

    if not next_action:
        result = {
            "generated_at": datetime.utcnow().isoformat(),
            "error": "no_next_action"
        }
        with open(OUTPUT_PATH, "w") as f:
            json.dump(result, f, indent=2)
        return

    execution = execute_action(next_action)

    result = {
        "generated_at": datetime.utcnow().isoformat(),
        "resolved_next_action": next_action,
        "execution": execution
    }

    # 🔥 AUTO-INGEST AFTER INSPECTION
    if execution.get("trigger_ingestion"):
        try:
            subprocess.run(
                ["python", "install/apply.py"],
                check=True
            )
            result["ingestion"] = {
                "status": "triggered"
            }
        except Exception as e:
            result["ingestion"] = {
                "status": "failed",
                "error": str(e)
            }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
