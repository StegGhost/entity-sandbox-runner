import os
import json
import zipfile
import tempfile
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


def repair_bundle_manifest(bundle_name, missing_fields, allowed_paths):
    src = os.path.join(FAILED_BUNDLES, bundle_name)

    if not os.path.exists(src):
        return {"status": "failed", "reason": "bundle_not_found"}

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
                with open(manifest_path, "r") as f:
                    manifest = json.load(f)
            except:
                manifest = {}

        if not manifest:
            manifest = {
                "bundle_name": bundle_name.replace(".zip", ""),
                "bundle_version": "1.0.0",
            }

        if "version" not in manifest:
            manifest["version"] = "1.0"

        if "install_mode" not in manifest:
            manifest["install_mode"] = "folder_map"

        if not manifest.get("allowed_paths"):
            manifest["allowed_paths"] = allowed_paths or ["bundle_manifest.json", "install/"]

        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        repaired_name = bundle_name.replace(".zip", "_manifest_fixed.zip")
        repaired_path = os.path.join(INCOMING_BUNDLES, repaired_name)

        with zipfile.ZipFile(repaired_path, "w") as zf:
            for root, _, files in os.walk(extract_root):
                for fname in files:
                    full = os.path.join(root, fname)
                    rel = os.path.relpath(full, extract_root)
                    zf.write(full, rel)

        return {
            "status": "ok",
            "repaired_bundle": repaired_name
        }


def local_install(bundle_name):
    src = os.path.join(INCOMING_BUNDLES, bundle_name)
    dst = os.path.join(INSTALLED_BUNDLES, bundle_name)

    ensure_dir(INSTALLED_BUNDLES)

    if not os.path.exists(src):
        return {"status": "failed", "reason": "missing_incoming_bundle"}

    os.rename(src, dst)

    return {"status": "installed", "path": dst}


def find_repairable_candidate(next_action_doc):
    candidates = next_action_doc.get("candidates", {})
    repairables = candidates.get("manifest_repairable", [])

    if not repairables:
        return None

    return repairables[0]


def main():
    ensure_dir(BRAIN_REPORTS)

    doc = load_json(NEXT_ACTION_PATH, {})
    action = doc.get("next_action", {}).get("action")
    target = doc.get("next_action", {}).get("target")

    result = {
        "generated_at": utc_now(),
        "input_document": doc
    }

    # 🔥 CRITICAL FIX: fallback if unsupported
    if action != "repair_bundle_manifest":
        fallback = find_repairable_candidate(doc)

        if fallback:
            action = "repair_bundle_manifest"
            target = fallback["bundle"]
            missing_fields = fallback.get("missing_fields", [])
            allowed_paths = fallback.get("allowed_paths", [])
        else:
            result["execution"] = {
                "status": "noop",
                "reason": "no_supported_actions_available"
            }
            write_json(OUTPUT_PATH, result)
            print(json.dumps(result, indent=2))
            return
    else:
        missing_fields = doc.get("next_action", {}).get("missing_fields", [])
        allowed_paths = doc.get("next_action", {}).get("allowed_paths", [])

    execution = repair_bundle_manifest(target, missing_fields, allowed_paths)

    result["execution"] = execution

    if execution.get("status") == "ok":
        install = local_install(execution["repaired_bundle"])
        result["local_install"] = install
    else:
        result["local_install"] = {"status": "skipped"}

    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
