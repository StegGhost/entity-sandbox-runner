import os
import json
import shutil
import zipfile
import tempfile
from datetime import datetime

ROOT = os.getcwd()

BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
FAILED_BUNDLES = os.path.join(ROOT, "failed_bundles")
INCOMING_BUNDLES = os.path.join(ROOT, "incoming_bundles")
INSTALLED_BUNDLES = os.path.join(ROOT, "installed_bundles")
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


def get_installed_families():
    ensure_dir(INSTALLED_BUNDLES)
    families = set()
    for f in os.listdir(INSTALLED_BUNDLES):
        if is_valid_bundle(f):
            families.add(family_key(f))
    return families


def default_allowed_paths_from_tree(extract_root):
    allowed = []

    for root, _, files in os.walk(extract_root):
        for fname in files:
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, extract_root).replace("\\", "/")

            if rel == "bundle_manifest.json":
                if "bundle_manifest.json" not in allowed:
                    allowed.append("bundle_manifest.json")
                continue

            if "/" in rel:
                top = rel.split("/", 1)[0]
                prefix = f"{top}/"
                if prefix not in allowed:
                    allowed.append(prefix)
            else:
                if rel not in allowed:
                    allowed.append(rel)

    if "bundle_manifest.json" not in allowed:
        allowed.insert(0, "bundle_manifest.json")

    return allowed


def repair_bundle_manifest(bundle_name, missing_fields, allowed_paths):
    src = os.path.join(FAILED_BUNDLES, os.path.basename(bundle_name))

    if not os.path.exists(src):
        return {
            "status": "failed",
            "executed": False,
            "reason": "bundle_not_found",
            "bundle": os.path.basename(bundle_name),
        }

    ensure_dir(INCOMING_BUNDLES)

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_root = os.path.join(tmpdir, "bundle")
        os.makedirs(extract_root, exist_ok=True)

        with zipfile.ZipFile(src, "r") as zf:
            zf.extractall(extract_root)

        manifest_path = os.path.join(extract_root, "bundle_manifest.json")
        manifest = {}

        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
            except Exception:
                manifest = {}

        if not manifest:
            stem = os.path.basename(bundle_name)
            if stem.endswith(".zip"):
                stem = stem[:-4]
            manifest = {
                "bundle_name": stem,
                "bundle_version": "1.0.0",
            }

        if "version" in missing_fields and "version" not in manifest:
            manifest["version"] = "1.0"

        if "install_mode" in missing_fields and "install_mode" not in manifest:
            manifest["install_mode"] = "folder_map"

        if "allowed_paths" in missing_fields and not manifest.get("allowed_paths"):
            manifest["allowed_paths"] = allowed_paths or default_allowed_paths_from_tree(extract_root)

        if not manifest.get("allowed_paths"):
            manifest["allowed_paths"] = allowed_paths or default_allowed_paths_from_tree(extract_root)

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")

        stem = os.path.basename(bundle_name)
        if stem.endswith(".zip"):
            stem = stem[:-4]
        repaired_name = f"{stem}_manifest_fixed.zip"
        repaired_path = os.path.join(INCOMING_BUNDLES, repaired_name)

        with zipfile.ZipFile(repaired_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(extract_root):
                for fname in files:
                    full = os.path.join(root, fname)
                    rel = os.path.relpath(full, extract_root).replace("\\", "/")
                    zf.write(full, rel)

        return {
            "status": "ok",
            "executed": True,
            "action": "repair_bundle_manifest",
            "target": os.path.basename(bundle_name),
            "bundle": repaired_name,
            "repaired_bundle": repaired_name,
            "repaired_path": repaired_path,
            "manifest_after_repair": manifest,
            "trigger_ingestion": True,
        }


def inspect_failed_bundle_family(target):
    src = os.path.join(ROOT, target) if not os.path.isabs(target) else target

    if not target or not os.path.exists(src):
        return {
            "status": "failed",
            "executed": False,
            "reason": "target_not_found",
            "target": target,
        }

    ensure_dir(INCOMING_BUNDLES)

    bundle_name = os.path.basename(src)
    dst = os.path.join(INCOMING_BUNDLES, bundle_name)

    try:
        shutil.move(src, dst)
    except Exception as e:
        return {
            "status": "failed",
            "executed": False,
            "reason": "move_failed",
            "error": str(e),
            "target": target,
        }

    return {
        "status": "ok",
        "executed": True,
        "action": "inspect_failed_bundle_family",
        "moved_to_incoming": dst,
        "bundle": bundle_name,
        "trigger_ingestion": True,
    }


def fallback_action(state):
    ensure_dir(FAILED_BUNDLES)

    installed_families = get_installed_families()
    candidates = []

    for f in os.listdir(FAILED_BUNDLES):
        if not is_valid_bundle(f):
            continue
        family = family_key(f)
        if family in installed_families:
            continue
        if is_family_exhausted(state, family):
            continue
        candidates.append((state["failures"].get(family, 0), f))

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x[0], x[1]))
    chosen = candidates[0][1]

    return {
        "action": "inspect_failed_bundle_family",
        "target": os.path.join("failed_bundles", chosen),
        "family": family_key(chosen),
        "source": "fallback_convergent",
    }


def main():
    ensure_dir(BRAIN_REPORTS)
    state = load_state()

    next_action_doc = load_json(NEXT_ACTION_PATH, {})
    next_action = next_action_doc.get("next_action", {})

    if not next_action:
        next_action = fallback_action(state) or {}

    action = next_action.get("action")
    target = next_action.get("target")
    missing_fields = next_action.get("missing_fields", [])
    allowed_paths = next_action.get("allowed_paths", [])

    result = {
        "generated_at": utc_now(),
        "input_document": next_action_doc,
        "resolved_next_action": next_action,
    }

    if not action or action == "idle":
        result["execution"] = {
            "status": "noop",
            "executed": False,
            "reason": "no_action_to_execute",
            "action": action,
            "target": target,
        }
        result["ingestion"] = {
            "status": "skipped",
            "reason": "no_action_to_execute",
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    if action == "repair_bundle_manifest":
        execution = repair_bundle_manifest(target, missing_fields, allowed_paths)
    elif action == "inspect_failed_bundle_family":
        execution = inspect_failed_bundle_family(target)
    else:
        execution = {
            "status": "failed",
            "executed": False,
            "reason": "unknown_or_unsupported_action",
            "action": action,
            "target": target,
        }

    result["execution"] = execution

    if execution.get("status") != "ok":
        record_failure(state, family_key(target))
        save_state(state)
        result["ingestion"] = {
            "status": "skipped",
            "reason": "execution_failed",
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    result["ingestion"] = {
        "status": "triggered" if execution.get("trigger_ingestion") else "skipped",
        "reason": "external_ingestion_pipeline" if execution.get("trigger_ingestion") else "no_trigger_requested",
    }

    save_state(state)
    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
