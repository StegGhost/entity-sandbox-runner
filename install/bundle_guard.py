import json
import os

REQUIRED_FIELDS = [
    "bundle_name",
    "version",
    "install_mode",
    "description",
    "allowed_paths",
]

ALLOWED_ROOTS = [
    "install/",
    "payload/",
    "experiments/",
    "workflow_review/",
]


def validate_manifest(manifest_path):
    if not os.path.exists(manifest_path):
        return False, "manifest_missing"

    with open(manifest_path, "r", encoding="utf-8") as f:
        try:
            manifest = json.load(f)
        except Exception:
            return False, "invalid_json"

    missing = [field for field in REQUIRED_FIELDS if field not in manifest]
    if missing:
        return False, f"missing_fields:{missing}"

    for path in manifest["allowed_paths"]:
        if path not in ALLOWED_ROOTS:
            return False, f"invalid_allowed_path:{path}"

    return True, "valid"


def validate_bundle(bundle_path):
    manifest_path = os.path.join(bundle_path, "bundle_manifest.json")
    valid, reason = validate_manifest(manifest_path)
    return {
        "valid": valid,
        "reason": reason,
        "bundle_path": bundle_path,
    }
