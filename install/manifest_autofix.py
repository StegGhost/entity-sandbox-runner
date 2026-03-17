import json

DEFAULT_ALLOWED_PATHS = [
    "install/",
    "payload/",
    "experiments/",
    "workflow_review/"
]

def autofix_manifest(manifest):
    modified = False

    if "allowed_paths" not in manifest:
        manifest["allowed_paths"] = DEFAULT_ALLOWED_PATHS
        modified = True

    if "install_mode" not in manifest:
        manifest["install_mode"] = "folder_map"
        modified = True

    return manifest, modified
