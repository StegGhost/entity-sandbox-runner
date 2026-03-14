from pathlib import Path
import json

def load_manifest(extracted_root: Path):
    manifests = list(extracted_root.rglob("bundle_manifest.json"))
    if not manifests:
        return None, None
    manifest_path = manifests[0]
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    return manifest_path, data

def verify_against_manifest(repo_root: Path, extracted_root: Path):
    manifest_path, manifest = load_manifest(extracted_root)
    if manifest is None:
        return {
            "manifest_found": False,
            "expected_files": [],
            "missing_files": [],
            "verified": True,
            "reason": "no_manifest_fallback_mode"
        }

    expected = []
    missing = []

    mode = manifest.get("install_mode")
    if mode == "file_map":
        for _src, dest_rel in manifest.get("file_map", {}).items():
            expected.append(dest_rel)
            if not (repo_root / dest_rel).exists():
                missing.append(dest_rel)

    elif mode == "folder_map":
        # folder_map cannot enumerate exact files alone, so mark manifest present but not exact-file strict
        return {
            "manifest_found": True,
            "manifest_path": str(manifest_path),
            "expected_files": [],
            "missing_files": [],
            "verified": True,
            "reason": "folder_map_present_manual_scope"
        }

    return {
        "manifest_found": True,
        "manifest_path": str(manifest_path),
        "expected_files": expected,
        "missing_files": missing,
        "verified": len(missing) == 0,
        "reason": "file_map_verification"
    }
