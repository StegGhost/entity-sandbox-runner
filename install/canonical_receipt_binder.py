import argparse
import hashlib
import json
import os
import time

INDEX_PATH = "docs/canonical/index.json"
DEFAULT_OUTPUT_ROOT = "payload/receipts/canonical_state"

DEFAULT_CONFIG = {
    "repo_state_paths": [
        "install",
        "config",
        "docs/canonical",
        "payload/feedback",
        "payload/knowledge_delta"
    ],
    "execution_receipts_root": "payload/receipts",
    "compaction_receipts_root": "payload/receipts/document_compaction",
    "feedback_receipts_root": "payload/receipts/canonical_feedback",
    "knowledge_delta_receipts_root": "payload/receipts/knowledge_delta",
    "canonical_index_path": "docs/canonical/index.json",
    "output_root": "payload/receipts/canonical_state"
}


def _norm(path):
    return path.replace("\\\\", "/")


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _sha256_obj(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()


def _load_json(path, default):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return default


def _collect_repo_state_hash(paths):
    items = []
    for root in paths:
        if not os.path.exists(root):
            continue
        for r, _, files in os.walk(root):
            for fn in sorted(files):
                full = os.path.join(r, fn)
                rel = _norm(os.path.relpath(full, "."))
                try:
                    with open(full, "rb") as f:
                        h = hashlib.sha256(f.read()).hexdigest()
                    items.append(f"{rel}:{h}")
                except Exception:
                    continue
    items.sort()
    return hashlib.sha256("\\n".join(items).encode("utf-8", errors="replace")).hexdigest(), items


def _latest_json_in(root, prefix):
    if not os.path.exists(root):
        return None, None
    cands = sorted(
        f for f in os.listdir(root)
        if f.startswith(prefix) and f.endswith(".json")
    )
    if not cands:
        return None, None
    name = cands[-1]
    path = os.path.join(root, name)
    return _norm(path), _load_json(path, {})


def build_canonical_state_receipt(config):
    output_root = config.get("output_root", DEFAULT_CONFIG["output_root"])
    os.makedirs(output_root, exist_ok=True)

    repo_state_hash, repo_state_items = _collect_repo_state_hash(config.get("repo_state_paths", []))

    compaction_path, compaction = _latest_json_in(config.get("compaction_receipts_root"), "document_compaction_")
    feedback_path, feedback = _latest_json_in(config.get("feedback_receipts_root"), "canonical_feedback_")
    delta_path, delta = _latest_json_in(config.get("knowledge_delta_receipts_root"), "knowledge_delta_")

    exec_root = config.get("execution_receipts_root", "payload/receipts")
    exec_receipts = []
    if os.path.exists(exec_root):
        for fn in sorted(os.listdir(exec_root)):
            if fn.startswith("r_") and fn.endswith(".json"):
                exec_receipts.append(_norm(os.path.join(exec_root, fn)))
    latest_execution_receipt = exec_receipts[-1] if exec_receipts else None

    index_path = config.get("canonical_index_path", INDEX_PATH)
    index = _load_json(index_path, {})
    previous_canonical_state_receipt = index.get("latest_canonical_state_receipt")

    receipt = {
        "type": "canonical_state",
        "timestamp": time.time(),
        "repo_state_hash": repo_state_hash,
        "repo_state_file_count": len(repo_state_items),
        "latest_execution_receipt": latest_execution_receipt,
        "document_compaction_receipt": compaction_path,
        "document_compaction_hash": compaction.get("hash"),
        "canonical_feedback_receipt": feedback_path,
        "canonical_feedback_hash": feedback.get("hash"),
        "knowledge_delta_receipt": delta_path,
        "knowledge_delta_hash": delta.get("hash"),
        "summary_hash": feedback.get("summary_hash") or compaction.get("summary_hash"),
        "previous_canonical_state_receipt": previous_canonical_state_receipt
    }
    receipt["hash"] = _sha256_obj(receipt)

    existing = sorted(
        f for f in os.listdir(output_root)
        if f.startswith("canonical_state_") and f.endswith(".json")
    )
    out_path = os.path.join(output_root, f"canonical_state_{len(existing)+1:04d}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    index["latest_repo_state_hash"] = repo_state_hash
    index["latest_summary_hash"] = receipt.get("summary_hash")
    index["latest_canonical_feedback_hash"] = receipt.get("canonical_feedback_hash")
    index["latest_knowledge_delta_hash"] = receipt.get("knowledge_delta_hash")
    index["latest_canonical_state_receipt"] = _norm(out_path)
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    result = {
        "status": "ok",
        "receipt_path": _norm(out_path),
        "repo_state_hash": repo_state_hash,
        "summary_hash": receipt.get("summary_hash"),
        "canonical_feedback_hash": receipt.get("canonical_feedback_hash"),
        "knowledge_delta_hash": receipt.get("knowledge_delta_hash"),
        "index_path": _norm(index_path)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main():
    parser = argparse.ArgumentParser(description="Bind canonical knowledge artifacts into a higher-order canonical state receipt.")
    parser.add_argument("--config", default="config/canonical_receipt_binder_config.json")
    args = parser.parse_args()
    cfg = _load_json(args.config, DEFAULT_CONFIG.copy())
    merged = DEFAULT_CONFIG.copy()
    if isinstance(cfg, dict):
        merged.update(cfg)
    build_canonical_state_receipt(merged)


if __name__ == "__main__":
    main()
