import os
import json
import zipfile
import tempfile
import subprocess
import time
import shutil
from datetime import datetime

ROOT = os.getcwd()

BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
FAILED_BUNDLES = os.path.join(ROOT, "failed_bundles")
INCOMING_BUNDLES = os.path.join(ROOT, "incoming_bundles")
INSTALLED_BUNDLES = os.path.join(ROOT, "installed_bundles")

NEXT_ACTION_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")


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


# -----------------------------
# NEW: INSPECT CAPABILITY
# -----------------------------
def inspect_failed_bundle_family(target):
    src = os.path.join(ROOT, target)

    if not os.path.exists(src):
        return {
            "status": "failed",
            "reason": "bundle_not_found",
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
    }


# -----------------------------
# EXISTING: MANIFEST REPAIR
# -----------------------------
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
    src = os.path.join(FAILED_BUNDLES, bundle_name)

    if not os.path.exists(src):
        return {
            "status": "failed",
            "reason": "bundle_not_found",
            "bundle": bundle_name,
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
            stem = bundle_name[:-4] if bundle_name.endswith(".zip") else bundle_name
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

        stem = bundle_name[:-4] if bundle_name.endswith(".zip") else bundle_name
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
            "target": bundle_name,
            "repaired_bundle": repaired_name,
            "repaired_path": repaired_path,
        }


# -----------------------------
# MAIN
# -----------------------------
def main():
    ensure_dir(BRAIN_REPORTS)

    next_action_doc = load_json(NEXT_ACTION_PATH, {})
    next_action = next_action_doc.get("next_action", {})

    action = next_action.get("action")
    target = next_action.get("target")
    missing_fields = next_action.get("missing_fields", [])
    allowed_paths = next_action.get("allowed_paths", [])

    result = {
        "generated_at": utc_now(),
        "resolved_next_action": next_action,
    }

    if not action or action == "idle":
        result["execution"] = {
            "status": "noop",
            "executed": False,
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    if action == "repair_bundle_manifest":
        execution = repair_bundle_manifest(
            os.path.basename(target),
            missing_fields,
            allowed_paths
        )

    elif action == "inspect_failed_bundle_family":
        execution = inspect_failed_bundle_family(target)

    else:
        execution = {
            "status": "failed",
            "executed": False,
            "reason": "unknown_action",
            "action": action,
        }

    result["execution"] = execution

    # optional auto-install if repaired
    if execution.get("status") == "ok" and execution.get("action") == "repair_bundle_manifest":
        repaired_path = execution.get("repaired_path")
        if repaired_path:
            ensure_dir(INSTALLED_BUNDLES)
            dst = os.path.join(INSTALLED_BUNDLES, os.path.basename(repaired_path))
            shutil.move(repaired_path, dst)

            result["local_install"] = {
                "status": "installed",
                "path": dst
            }

    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
