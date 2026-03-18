import hashlib
import json
import os
import shutil
import time

STAGING_ROOT = "payload/repo_root"
LOG_PATH = "logs/repo_root_promotions.json"
RULES_PATH = "config/repo_root_promoter_rules.json"

DEFAULT_RULES = {
    "exact_files": [
        "README.md",
        "architecture_map.md"
    ],
    "prefixes": [
        "docs/"
    ],
    "allow_workflows": False
}

def _ensure():
    os.makedirs("logs", exist_ok=True)

def _load_rules():
    if not os.path.exists(RULES_PATH) or os.path.getsize(RULES_PATH) == 0:
        return DEFAULT_RULES.copy()
    try:
        with open(RULES_PATH, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return DEFAULT_RULES.copy()
        out = DEFAULT_RULES.copy()
        for key in ("exact_files", "prefixes", "allow_workflows"):
            if key in data:
                out[key] = data[key]
        return out
    except Exception:
        return DEFAULT_RULES.copy()

def _load_log():
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0:
        return []
    try:
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []

def _save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def _sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def _is_allowed(rel_path, rules):
    if rel_path in rules.get("exact_files", []):
        return True
    for prefix in rules.get("prefixes", []):
        if rel_path.startswith(prefix):
            return True
    if rel_path.startswith(".github/workflows/"):
        return bool(rules.get("allow_workflows", False))
    return False

def promote():
    _ensure()
    rules = _load_rules()
    log = _load_log()

    result = {
        "status": "pass",
        "promoted": [],
        "skipped": [],
        "missing_staging_root": False,
        "ts": time.time()
    }

    if not os.path.exists(STAGING_ROOT):
        result["missing_staging_root"] = True
        log.append(result)
        _save_log(log)
        return result

    for root, _, files in os.walk(STAGING_ROOT):
        for file in files:
            src = os.path.join(root, file)
            rel = os.path.relpath(src, STAGING_ROOT)

            if not _is_allowed(rel, rules):
                result["skipped"].append({
                    "path": rel,
                    "reason": "not_allowed"
                })
                continue

            dst = rel
            if dst == ".git" or dst.startswith(".git/"):
                result["skipped"].append({
                    "path": rel,
                    "reason": "forbidden_destination"
                })
                continue

            parent = os.path.dirname(dst)
            if parent:
                os.makedirs(parent, exist_ok=True)

            before_hash = _sha256_file(dst)
            shutil.copy2(src, dst)
            after_hash = _sha256_file(dst)

            result["promoted"].append({
                "from": src,
                "to": dst,
                "before_hash": before_hash,
                "after_hash": after_hash
            })

    log.append(result)
    _save_log(log)
    return result

if __name__ == "__main__":
    print(json.dumps(promote(), indent=2))
