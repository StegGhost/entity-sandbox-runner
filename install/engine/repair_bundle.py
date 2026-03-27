import os
import json
import zipfile
import shutil
import hashlib
from datetime import datetime

FAILED_DIR = "failed_bundles"
REPAIRED_DIR = "repaired_bundles"
TMP_DIR = "_repair_tmp"
REPORT_PATH = "brain_reports/repair_bundle_result.json"


def now():
    return datetime.utcnow().isoformat() + "Z"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def ensure_dirs():
    os.makedirs(FAILED_DIR, exist_ok=True)
    os.makedirs(REPAIRED_DIR, exist_ok=True)
    os.makedirs("brain_reports", exist_ok=True)


def unzip_bundle(bundle_path, extract_to):
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)
    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(bundle_path, "r") as z:
        z.extractall(extract_to)


def zip_bundle(folder_path, output_path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full = os.path.join(root, file)
                rel = os.path.relpath(full, folder_path)
                z.write(full, rel)


def load_manifest(root):
    manifest_path = os.path.join(root, "bundle_manifest.json")
    if not os.path.exists(manifest_path):
        return None, manifest_path

    try:
        with open(manifest_path, "r") as f:
            return json.load(f), manifest_path
    except Exception:
        return None, manifest_path


def write_manifest(manifest_path, data):
    with open(manifest_path, "w") as f:
        json.dump(data, f, indent=2)


def fix_manifest(manifest):
    changed = False

    # Required fields (minimal deterministic schema)
    required_defaults = {
        "bundle_name": "unknown_bundle",
        "bundle_version": "0.0.1",
        "status": "repaired",
        "capabilities": {},
        "files": []
    }

    for key, default in required_defaults.items():
        if key not in manifest:
            manifest[key] = default
            changed = True

    return manifest, changed


def derive_family(bundle_name):
    if not bundle_name:
        return "unknown"
    parts = bundle_name.split("_")
    return "_".join(parts[:3]) if len(parts) >= 3 else bundle_name


def repair_bundle(bundle_path):
    ensure_dirs()

    bundle_name = os.path.basename(bundle_path)
    tmp_extract = os.path.join(TMP_DIR, bundle_name)

    result = {
        "ts": now(),
        "status": "failed",
        "input_bundle": bundle_path,
        "output_bundle": None,
        "changes_applied": [],
        "errors": [],
        "family": None,
        "hash_before": None,
        "hash_after": None
    }

    try:
        result["hash_before"] = sha256_file(bundle_path)

        unzip_bundle(bundle_path, tmp_extract)

        manifest, manifest_path = load_manifest(tmp_extract)

        if manifest is None:
            # create minimal manifest
            manifest = {
                "bundle_name": bundle_name.replace(".zip", ""),
                "bundle_version": "0.0.1",
                "status": "repaired",
                "capabilities": {},
                "files": []
            }
            write_manifest(manifest_path, manifest)
            result["changes_applied"].append("created_missing_manifest")

        else:
            manifest, changed = fix_manifest(manifest)
            if changed:
                write_manifest(manifest_path, manifest)
                result["changes_applied"].append("fixed_manifest_fields")

        result["family"] = derive_family(manifest.get("bundle_name"))

        repaired_path = os.path.join(REPAIRED_DIR, bundle_name)

        zip_bundle(tmp_extract, repaired_path)

        result["output_bundle"] = repaired_path
        result["hash_after"] = sha256_file(repaired_path)
        result["status"] = "repaired"

    except Exception as e:
        result["errors"].append(str(e))

    finally:
        if os.path.exists(tmp_extract):
            shutil.rmtree(tmp_extract)

    with open(REPORT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps({
        "status": result["status"],
        "output": REPORT_PATH,
        "result": result
    }))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Path to failed bundle zip")
    args = parser.parse_args()

    repair_bundle(args.target)
