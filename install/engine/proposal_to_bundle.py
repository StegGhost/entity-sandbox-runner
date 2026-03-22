
import os

def normalize_allowed_paths(bundle_root: str):
    allowed = set()

    has_install = False
    has_config = False
    has_docs = False

    for root, dirs, files in os.walk(bundle_root):
        rel_root = os.path.relpath(root, bundle_root)
        if rel_root == ".":
            rel_root = ""

        # Detect top-level domains
        if rel_root.startswith("install"):
            has_install = True
        if rel_root.startswith("config"):
            has_config = True
        if rel_root.startswith("docs"):
            has_docs = True

    # Always include manifest correctly as file
    allowed.add("bundle_manifest.json")

    # Collapse scopes
    if has_install:
        allowed.add("install/")
    if has_config:
        allowed.add("config/")
    if has_docs:
        allowed.add("docs/")

    return sorted(list(allowed))


def build_manifest(bundle_root: str):
    allowed_paths = normalize_allowed_paths(bundle_root)

    manifest = {
        "bundle_name": os.path.basename(bundle_root),
        "bundle_version": "2.0.0",
        "install_mode": "folder_map",
        "allowed_paths": allowed_paths
    }

    return manifest


if __name__ == "__main__":
    root = os.getcwd()
    manifest = build_manifest(root)
    print(manifest)
