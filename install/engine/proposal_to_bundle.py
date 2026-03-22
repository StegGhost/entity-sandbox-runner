
import json
import os
import shutil

ALLOWED_PATHS = [
    "bundle_manifest.json",
    "install/tests/",
    "install/engine/",
    "install/apply.py"
]

MAX_RETRIES = 3

def build_manifest(bundle_name, bundle_version="1.0.0"):
    return {
        "bundle_name": bundle_name,
        "bundle_version": bundle_version,
        "install_mode": "folder_map",
        "allowed_paths": ALLOWED_PATHS
    }

def simulate_ingestion(bundle_root):
    manifest_path = os.path.join(bundle_root, "bundle_manifest.json")
    if not os.path.exists(manifest_path):
        return False, "missing_manifest"

    with open(manifest_path) as f:
        manifest = json.load(f)

    allowed = manifest.get("allowed_paths", [])

    for root, _, files in os.walk(bundle_root):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), bundle_root)

            if rel_path == "bundle_manifest.json":
                continue

            valid = False
            for path in allowed:
                if path.endswith("/") and rel_path.startswith(path):
                    valid = True
                elif rel_path == path:
                    valid = True

            if not valid:
                return False, f"capability_violation:{rel_path}"

    return True, "ok"

def ensure_structure(bundle_root):
    os.makedirs(os.path.join(bundle_root, "install/tests"), exist_ok=True)
    os.makedirs(os.path.join(bundle_root, "install/engine"), exist_ok=True)

    apply_path = os.path.join(bundle_root, "install/apply.py")
    if not os.path.exists(apply_path):
        with open(apply_path, "w") as f:
            f.write("def apply():\n    print(\"Bundle applied successfully.\")\n")

def auto_repair(bundle_root, reason):
    if reason.startswith("capability_violation:"):
        bad_path = reason.split(":", 1)[1]
        full_path = os.path.join(bundle_root, bad_path)

        quarantine_dir = os.path.join(bundle_root, "quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)

        if os.path.exists(full_path):
            shutil.move(full_path, os.path.join(quarantine_dir, os.path.basename(bad_path)))
        return True

    if reason == "missing_manifest":
        return True

    return False

def build_bundle(bundle_root, bundle_name):
    ensure_structure(bundle_root)

    manifest = build_manifest(bundle_name)
    with open(os.path.join(bundle_root, "bundle_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    for _ in range(MAX_RETRIES):
        ok, reason = simulate_ingestion(bundle_root)
        if ok:
            return True

        repaired = auto_repair(bundle_root, reason)
        if not repaired:
            raise Exception(f"UNRECOVERABLE:{reason}")

    raise Exception(f"MAX_RETRIES_EXCEEDED:{reason}")
