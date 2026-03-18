import os
import json
import hashlib
import shutil

MANIFEST_PATH = "config/repo_integrity_manifest.json"
CANONICAL_ROOT = "payload/canonical"
INTEGRITY_DIR = "payload/integrity"


def sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None


def load_json_safe(path):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return None
        with open(path) as f:
            return json.load(f)
    except:
        return None


def ensure_json_schema(path, defaults):
    data = load_json_safe(path) or {}

    repaired = False
    for k, v in defaults.items():
        if k not in data:
            data[k] = v
            repaired = True

    if repaired:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    return repaired


def replace_from_canonical(path, canonical_path):
    if not os.path.exists(canonical_path):
        return False

    os.makedirs(os.path.dirname(path), exist_ok=True)
    shutil.copyfile(canonical_path, path)
    return True


def check_contains(path, required_strings):
    if not os.path.exists(path):
        return False

    try:
        with open(path) as f:
            content = f.read()
        return all(s in content for s in required_strings)
    except:
        return False


def run_integrity_check():
    manifest = load_json_safe(MANIFEST_PATH)
    if not manifest:
        return {"status": "fail", "reason": "missing_manifest"}

    results = []
    file_hashes = []
    repaired = 0
    failed = 0

    for entry in manifest.get("files", []):
        path = entry["path"]
        mode = entry["mode"]

        status = "ok"
        action = None

        if mode == "exists":
            if not os.path.exists(path):
                status = "missing"
                failed += 1

        elif mode == "contains":
            if not check_contains(path, entry.get("required_strings", [])):
                status = "repair_needed"
                if entry.get("canonical_path"):
                    replaced = replace_from_canonical(
                        path,
                        os.path.join(CANONICAL_ROOT, entry["canonical_path"])
                    )
                    if replaced:
                        status = "repaired"
                        action = "replaced_from_canonical"
                        repaired += 1
                    else:
                        failed += 1

        elif mode == "json_schema":
            if ensure_json_schema(path, entry.get("defaults", {})):
                status = "repaired"
                action = "schema_fixed"
                repaired += 1

        elif mode == "replace":
            replaced = replace_from_canonical(
                path,
                os.path.join(CANONICAL_ROOT, entry["canonical_path"])
            )
            if replaced:
                status = "replaced"
                action = "forced_replace"
                repaired += 1
            else:
                status = "failed"
                failed += 1

        file_hash = sha256_file(path)
        if file_hash:
            file_hashes.append(f"{path}:{file_hash}")

        results.append({
            "path": path,
            "status": status,
            "action": action
        })

    # 🔐 Deterministic repo hash
    file_hashes_sorted = sorted(file_hashes)
    combined = "\n".join(file_hashes_sorted)
    repo_hash = hashlib.sha256(combined.encode()).hexdigest()

    status = "pass"
    if failed > 0:
        status = "fail"
    elif repaired > 0:
        status = "pass_after_repair"

    receipt = {
        "receipt_type": "repo_integrity",
        "status": status,
        "checked_files": len(results),
        "repaired_files": repaired,
        "failed_files": failed,
        "repo_integrity_hash": repo_hash,
        "files": results
    }

    os.makedirs(INTEGRITY_DIR, exist_ok=True)

    existing = sorted(os.listdir(INTEGRITY_DIR))
    idx = len(existing) + 1

    path = os.path.join(INTEGRITY_DIR, f"integrity_{idx:04d}.json")
    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    return receipt
