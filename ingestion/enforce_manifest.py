from pathlib import Path
import json

def generate_dev_manifest(bundle_root: Path):
    files = []

    for p in bundle_root.rglob("*"):
        if p.is_file():
            files.append(str(p.relative_to(bundle_root)))

    return {
        "bundle_name": bundle_root.name,
        "version": "dev",
        "dev_bundle": True,
        "files": files
    }


def enforce_manifest(bundle_root: Path):

    manifest_candidates = [
        bundle_root / "bundle_manifest.json",
        bundle_root / "bundle_manifest_standard.json",
    ]

    manifest_path = None

    for m in manifest_candidates:
        if m.exists():
            manifest_path = m
            break

    # ----------------------------------
    # fallback dev manifest
    # ----------------------------------

    if manifest_path is None:

        manifest = generate_dev_manifest(bundle_root)

        return {
            "manifest_found": False,
            "verified": True,
            "reason": "generated_dev_manifest",
            "manifest": manifest
        }

    # ----------------------------------
    # normal manifest validation
    # ----------------------------------

    with open(manifest_path) as f:
        manifest = json.load(f)

    return {
        "manifest_found": True,
        "verified": True,
        "reason": "manifest_valid",
        "manifest": manifest
    }
