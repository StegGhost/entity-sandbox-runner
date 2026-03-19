import difflib
import hashlib
import json
import os
import shutil
import time

STAGING_ROOT = "payload/repo_root"
LOG_PATH = "logs/repo_root_promotions.json"
RECEIPT_DIR = "payload/integrity/promotions"
RULES_PATH = "config/repo_root_promoter_rules.json"

DEFAULT_RULES = {
    "exact_files": [
        "README.md",
        "architecture_map.md"
    ],
    "prefixes": [
        "docs/"
    ],
    "allow_workflows": False,
    "max_diff_lines": 200
}

def _ensure():
    os.makedirs("logs", exist_ok=True)
    os.makedirs(RECEIPT_DIR, exist_ok=True)

def _load_rules():
    if not os.path.exists(RULES_PATH) or os.path.getsize(RULES_PATH) == 0:
        return DEFAULT_RULES.copy()
    try:
        with open(RULES_PATH, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return DEFAULT_RULES.copy()
        out = DEFAULT_RULES.copy()
        for key in ("exact_files", "prefixes", "allow_workflows", "max_diff_lines"):
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

def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def _sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def _read_text_lines(path):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except Exception:
        return []

def _is_allowed(rel_path, rules):
    if rel_path in rules.get("exact_files", []):
        return True
    for prefix in rules.get("prefixes", []):
        if rel_path.startswith(prefix):
            return True
    if rel_path.startswith(".github/workflows/"):
        return bool(rules.get("allow_workflows", False))
    return False

def _build_diff(before_lines, after_lines, rel_path, max_lines):
    diff = list(difflib.unified_diff(
        before_lines,
        after_lines,
        fromfile=f"before/{rel_path}",
        tofile=f"after/{rel_path}",
        lineterm=""
    ))
    truncated = False
    if len(diff) > max_lines:
        diff = diff[:max_lines]
        truncated = True
    return diff, truncated

def _next_receipt_path():
    existing = sorted(
        f for f in os.listdir(RECEIPT_DIR)
        if f.startswith("promotion_") and f.endswith(".json")
    )
    idx = len(existing) + 1
    return os.path.join(RECEIPT_DIR, f"promotion_{idx:04d}.json")

def promote():
    _ensure()
    rules = _load_rules()
    log = _load_log()

    result = {
        "status": "pass",
        "promoted": [],
        "skipped": [],
        "missing_staging_root": False,
        "receipt_path": None,
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
            before_lines = _read_text_lines(dst)
            after_lines = _read_text_lines(src)

            shutil.copy2(src, dst)

            after_hash = _sha256_file(dst)
            diff_lines, truncated = _build_diff(before_lines, after_lines, rel, int(rules.get("max_diff_lines", 200)))

            result["promoted"].append({
                "from": src,
                "to": dst,
                "before_hash": before_hash,
                "after_hash": after_hash,
                "changed": before_hash != after_hash,
                "diff_truncated": truncated,
                "diff": diff_lines
            })

    receipt_body = {
        "type": "repo_root_promotion",
        "timestamp": result["ts"],
        "promoted_count": len(result["promoted"]),
        "skipped_count": len(result["skipped"]),
        "promoted": result["promoted"],
        "skipped": result["skipped"]
    }
    receipt_body["hash"] = _sha256_bytes(json.dumps(receipt_body, sort_keys=True).encode())
    receipt_path = _next_receipt_path()
    with open(receipt_path, "w") as f:
        json.dump(receipt_body, f, indent=2)

    result["receipt_path"] = receipt_path
    log.append(result)
    _save_log(log)
    return result

if __name__ == "__main__":
    print(json.dumps(promote(), indent=2))
