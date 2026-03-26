import json
import os
import shutil
import zipfile
from datetime import datetime

ROOT = os.getcwd()

BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
INCOMING_BUNDLES = os.path.join(ROOT, "incoming_bundles")
INSTALLED_BUNDLES = os.path.join(ROOT, "installed_bundles")
FAILED_BUNDLES = os.path.join(ROOT, "failed_bundles")
STATE_PATH = os.path.join(ROOT, "brain_state.json")

NEXT_ACTION_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")

FAILURE_THRESHOLD = 3


def utc_now():
    return datetime.utcnow().isoformat()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_json(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, payload):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def load_state():
    return load_json(STATE_PATH, {"failures": {}})


def save_state(state):
    write_json(STATE_PATH, state)


def is_valid_bundle(filename):
    return filename.endswith(".zip") and not filename.startswith(".")


def family_key(name):
    if not name:
        return None
    name = os.path.basename(name)
    if name.endswith(".zip"):
        name = name[:-4]
    for suffix in ["_manifest_fixed", "_fixed", "_bundle"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    if "_v" in name:
        name = name.split("_v")[0]
    return name


def record_failure(state, family):
    if not family:
        return
    state["failures"][family] = state["failures"].get(family, 0) + 1


def is_family_exhausted(state, family):
    return state["failures"].get(family, 0) >= FAILURE_THRESHOLD


def first_bundle_from(directory):
    ensure_dir(directory)
    bundles = sorted([f for f in os.listdir(directory) if is_valid_bundle(f)])
    return bundles[0] if bundles else None


def validate_bundle_zip(path):
    if not os.path.exists(path):
        return False, "bundle_not_found"

    if not zipfile.is_zipfile(path):
        return False, "invalid_zip"

    try:
        with zipfile.ZipFile(path, "r") as zf:
            names = zf.namelist()
            if "bundle_manifest.json" not in names:
                return False, "missing_manifest"
    except Exception as e:
        return False, f"zip_read_error:{e}"

    return True, "ok"


def process_incoming_bundle(state):
    bundle = first_bundle_from(INCOMING_BUNDLES)
    if not bundle:
        return {
            "status": "failed",
            "executed": False,
            "reason": "no_incoming_bundle",
        }

    src = os.path.join(INCOMING_BUNDLES, bundle)
    family = family_key(bundle)

    valid, reason = validate_bundle_zip(src)
    if not valid:
        ensure_dir(FAILED_BUNDLES)
        dst = os.path.join(FAILED_BUNDLES, bundle)
        shutil.move(src, dst)
        record_failure(state, family)
        return {
            "status": "failed",
            "executed": True,
            "action": "process_incoming_bundle",
            "bundle": bundle,
            "family": family,
            "reason": reason,
            "moved_to_failed": dst,
        }

    ensure_dir(INSTALLED_BUNDLES)
    dst = os.path.join(INSTALLED_BUNDLES, bundle)
    shutil.move(src, dst)

    return {
        "status": "ok",
        "executed": True,
        "action": "process_incoming_bundle",
        "bundle": bundle,
        "family": family,
        "reason": "installed",
        "installed_path": dst,
    }


def requeue_failed_bundle(state):
    ensure_dir(FAILED_BUNDLES)
    candidates = []

    for name in sorted(os.listdir(FAILED_BUNDLES)):
        if not is_valid_bundle(name):
            continue
        family = family_key(name)
        if is_family_exhausted(state, family):
            continue
        candidates.append((family, name))

    if not candidates:
        return {
            "status": "failed",
            "executed": False,
            "reason": "no_requeue_candidate",
        }

    _, bundle = candidates[0]
    src = os.path.join(FAILED_BUNDLES, bundle)

    ensure_dir(INCOMING_BUNDLES)
    dst = os.path.join(INCOMING_BUNDLES, bundle)
    shutil.move(src, dst)

    return {
        "status": "ok",
        "executed": True,
        "action": "requeue_failed_bundle",
        "bundle": bundle,
        "family": family_key(bundle),
        "reason": "requeued_from_failed",
        "moved_to_incoming": dst,
    }


def await_settlement():
    return {
        "status": "ok",
        "executed": False,
        "action": "await_settlement",
        "reason": "waiting_for_reconciliation",
    }


def idle():
    return {
        "status": "ok",
        "executed": False,
        "action": "idle",
        "reason": "no_action_to_execute",
    }


def main():
    ensure_dir(BRAIN_REPORTS)
    ensure_dir(INCOMING_BUNDLES)
    ensure_dir(INSTALLED_BUNDLES)
    ensure_dir(FAILED_BUNDLES)

    state = load_state()
    next_action_doc = load_json(NEXT_ACTION_PATH, {})
    next_action = next_action_doc.get("next_action", {}) or {}

    action = next_action.get("action")

    if action == "process_incoming_bundle":
        execution = process_incoming_bundle(state)
    elif action == "requeue_failed_bundle":
        execution = requeue_failed_bundle(state)
    elif action == "await_settlement":
        execution = await_settlement()
    else:
        execution = idle()

    result = {
        "generated_at": utc_now(),
        "input_document": next_action_doc,
        "resolved_next_action": next_action,
        "execution": execution,
    }

    save_state(state)
    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
