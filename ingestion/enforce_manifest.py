import json
import hashlib
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def enforce_manifest(bundle_root: Path):

    manifest_path = bundle_root / "bundle_manifest.json"

    if not manifest_path.exists():
        return {
            "manifest_found": False,
            "verified": False,
            "reason": "manifest_required"
        }

    manifest = json.loads(manifest_path.read_text())

    expected = manifest.get("files", [])

    missing = []
    hash_mismatch = []

    for f in expected:

        path = bundle_root / f["path"]

        if not path.exists():
            missing.append(f["path"])
            continue

        expected_hash = f["sha256"]

        if expected_hash == "AUTO":
            continue

        actual = sha256(path)

        if actual != expected_hash:
            hash_mismatch.append(f["path"])

    verified = not missing and not hash_mismatch

    return {
        "manifest_found": True,
        "verified": verified,
        "missing_files": missing,
        "hash_mismatch": hash_mismatch,
        "manifest": manifest
    }
