import json
from manifest_autofix import autofix_manifest

def preprocess_manifest(path):
    with open(path, "r") as f:
        manifest = json.load(f)

    fixed_manifest, modified = autofix_manifest(manifest)

    if modified:
        with open(path, "w") as f:
            json.dump(fixed_manifest, f, indent=2)

    return {
        "autofixed": modified,
        "manifest": fixed_manifest
    }
