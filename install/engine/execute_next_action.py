import os
import json
import shutil
import subprocess
from datetime import datetime


BRAIN_REPORT_PATH = "internal_brain/brain_report.json"
OUTPUT_PATH = "brain_reports/execute_next_action_result.json"

FAILED_DIR = "failed_bundles"
INCOMING_DIR = "incoming_bundles"
INSTALLED_DIR = "installed_bundles"

STATE_PATH = "brain_state.json"

FAILURE_THRESHOLD = 3


# -------------------------
# STATE
# -------------------------

def load_state():
    if not os.path.exists(STATE_PATH):
        return {"failures": {}}
    with open(STATE_PATH, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


# -------------------------
# HELPERS
# -------------------------

def load_brain_report():
    if not os.path.exists(BRAIN_REPORT_PATH):
        return None
    with open(BRAIN_REPORT_PATH, "r") as f:
        return json.load(f)


def ensure_dirs():
    os.makedirs("brain_reports", exist_ok=True)
    os.makedirs(INCOMING_DIR, exist_ok=True)
    os.makedirs(INSTALLED_DIR, exist_ok=True)


def is_valid_bundle(filename):
    return filename.endswith(".zip") and not filename.startswith(".")


def extract_family(filename):
    return filename.split("_v")[0]


def get_installed_families():
    if not os.path.exists(INSTALLED_DIR):
        return set()

    families = set()
    for f in os.listdir(INSTALLED_DIR):
        if f.endswith(".zip"):
            families.add(extract_family(f))
    return families


# -------------------------
# FAILURE TRACKING
# -------------------------

def record_failure(state, family):
    state["failures"][family] = state["failures"].get(family, 0) + 1


def is_family_exhausted(state, family):
    return state["failures"].get(family, 0) >= FAILURE_THRESHOLD


# -------------------------
# ACTION
# -------------------------

def inspect_failed_bundle_family(target):
    if not target or not os.path.exists(target):
        return {
            "status": "failed",
            "executed": False,
            "reason": "target_not_found"
        }

    bundle_name = os.path.basename(target)
    dst = os.path.join(INCOMING_DIR, bundle_name)

    try:
        shutil.move(target, dst)
    except Exception as e:
        return {
            "status": "failed",
            "executed": False,
            "reason": str(e)
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
        "reason": "unknown_action"
    }


# -------------------------
# SMART FALLBACK (WITH CONVERGENCE)
# -------------------------

def fallback_action(state):
    if not os.path.exists(FAILED_DIR):
        return None

    installed = get_installed_families()

    candidates = []

    for f in os.listdir(FAILED_DIR):
        if not is_valid_bundle(f):
            continue

        family = extract_family(f)

        if family in installed:
            continue

        if is_family_exhausted(state, family):
            continue

        candidates.append((family, f))

    if not candidates:
        return None

    # pick lowest failure count first
    candidates.sort(key=lambda x: state["failures"].get(x[0], 0))

    chosen = candidates[0][1]

    return {
        "action": "inspect_failed_bundle_family",
        "target": os.path.join(FAILED_DIR, chosen),
        "source": "fallback_convergent"
    }


# -------------------------
# MAIN
# -------------------------

def main():
    ensure_dirs()

    state = load_state()
    brain = load_brain_report()

    next_action = None
    if brain:
        next_action = brain.get("next_action")

    if not next_action:
        next_action = fallback_action(state)

    if not next_action:
        result = {
            "generated_at": datetime.utcnow().isoformat(),
            "status": "converged",
            "reason": "no_remaining_viable_bundles"
        }
        save_state(state)
        with open(OUTPUT_PATH, "w") as f:
            json.dump(result, f, indent=2)
        return

    execution = execute_action(next_action)

    # record failures
    if not execution.get("executed"):
        family = extract_family(os.path.basename(next_action.get("target", "")))
        record_failure(state, family)

    result = {
        "generated_at": datetime.utcnow().isoformat(),
        "resolved_next_action": next_action,
        "execution": execution
    }

    if execution.get("trigger_ingestion"):
        try:
            subprocess.run(
                ["python", "install/apply.py"],
                check=True
            )
            result["ingestion"] = {"status": "triggered"}
        except Exception as e:
            family = extract_family(execution.get("bundle", ""))
            record_failure(state, family)
            result["ingestion"] = {
                "status": "failed",
                "error": str(e)
            }

    save_state(state)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
