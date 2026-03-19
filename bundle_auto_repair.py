import json

REQUIRED_FIELDS = ["bundle_name", "version", "install_mode", "allowed_paths"]

def repair_manifest(path):
    with open(path, "r") as f:
        manifest = json.load(f)

    changed = False

    if "version" not in manifest:
        manifest["version"] = "1.0.0"
        changed = True

    if "install_mode" not in manifest:
        manifest["install_mode"] = "folder_map"
        changed = True

    if "allowed_paths" not in manifest:
        manifest["allowed_paths"] = [
            "bundle_manifest.json",
            "install/",
            "config/",
            "docs/"
        ]
        changed = True

    if changed:
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2)

    return changed
