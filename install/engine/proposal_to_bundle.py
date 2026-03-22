
import json
import os
from datetime import datetime

ALLOWED_PATHS = [
    "bundle_manifest.json",
    "install/tests/",
    "install/engine/",
    "install/apply.py"
]

def build_manifest(bundle_name, bundle_version="1.0.0"):
    return {
        "bundle_name": bundle_name,
        "bundle_version": bundle_version,
        "install_mode": "folder_map",
        "allowed_paths": ALLOWED_PATHS
    }

def write_manifest(bundle_root, manifest):
    path = os.path.join(bundle_root, "bundle_manifest.json")
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)

def build_bundle(bundle_root, bundle_name):
    manifest = build_manifest(bundle_name)
    write_manifest(bundle_root, manifest)

    # ensure required structure exists
    required_paths = [
        "install/tests",
        "install/engine"
    ]
    for p in required_paths:
        full_path = os.path.join(bundle_root, p)
        os.makedirs(full_path, exist_ok=True)

    # ensure apply.py exists
    apply_path = os.path.join(bundle_root, "install/apply.py")
    if not os.path.exists(apply_path):
        with open(apply_path, "w") as f:
            f.write(DEFAULT_APPLY)

    return True

DEFAULT_APPLY = '''def apply():
    print("Bundle applied successfully.")
'''
