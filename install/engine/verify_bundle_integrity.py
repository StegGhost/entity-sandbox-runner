
import json
import hashlib
from pathlib import Path

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_files(extracted_root, manifest):
    errors = []
    for f in manifest.get("files", []):
        path = extracted_root / f["path"]
        if not path.exists():
            errors.append(f"missing_file:{f['path']}")
            continue
        actual = sha256_file(path)
        if actual != f["sha256"]:
            errors.append(f"hash_mismatch:{f['path']}")
    return errors

def compute_manifest_hash(manifest):
    canonical = json.dumps(manifest, sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def verify_integrity(extracted_root, manifest):
    file_errors = verify_files(extracted_root, manifest)

    manifest_hash = compute_manifest_hash({
        k: v for k, v in manifest.items() if k != "signature"
    })

    return {
        "file_errors": file_errors,
        "manifest_hash": manifest_hash,
        "valid": not file_errors
    }
