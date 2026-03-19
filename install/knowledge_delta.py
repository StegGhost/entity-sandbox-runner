import argparse
import hashlib
import json
import os
import time

DEFAULT_CANONICAL_ROOT = "docs/canonical"
DEFAULT_OUTPUT_ROOT = "payload/knowledge_delta"
DEFAULT_RECEIPTS_ROOT = "payload/receipts/knowledge_delta"
INDEX_PATH = "docs/canonical/index.json"


def _sha256_obj(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()


def _load_json(path, default):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return default


def _read_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return [line.strip() for line in f.readlines()]
    except Exception:
        return []


def _extract_items(lines):
    out = []
    for line in lines:
        if line[:2].isdigit() and ". " in line:
            out.append(line.split(". ", 1)[1].strip())
        elif line.startswith("- "):
            out.append(line[2:].strip())
    # preserve order + dedupe
    seen = set()
    deduped = []
    for item in out:
        key = " ".join(item.lower().split())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def build_delta(canonical_root=DEFAULT_CANONICAL_ROOT, output_root=DEFAULT_OUTPUT_ROOT, receipts_root=DEFAULT_RECEIPTS_ROOT):
    os.makedirs(output_root, exist_ok=True)
    os.makedirs(receipts_root, exist_ok=True)

    summary = _load_json(os.path.join(canonical_root, "compaction_summary.json"), {})
    current_summary_hash = summary.get("summary_hash")

    claims = _extract_items(_read_lines(os.path.join(canonical_root, "claims_canonical.md")))
    definitions = _extract_items(_read_lines(os.path.join(canonical_root, "definitions_canonical.md")))
    findings = _extract_items(_read_lines(os.path.join(canonical_root, "findings_canonical.md")))

    current_state = {
        "summary_hash": current_summary_hash,
        "claims": claims,
        "definitions": definitions,
        "findings": findings
    }
    current_state_hash = _sha256_obj(current_state)

    index = _load_json(INDEX_PATH, {})
    previous = index.get("latest_knowledge_state", {})
    previous_state = {
        "summary_hash": previous.get("summary_hash"),
        "claims": previous.get("claims", []),
        "definitions": previous.get("definitions", []),
        "findings": previous.get("findings", [])
    }
    previous_state_hash = _sha256_obj(previous_state)

    def diff_lists(prev, curr):
        prev_set = set(prev)
        curr_set = set(curr)
        return {
            "added": [x for x in curr if x not in prev_set],
            "removed": [x for x in prev if x not in curr_set]
        }

    delta = {
        "timestamp": time.time(),
        "previous_summary_hash": previous.get("summary_hash"),
        "current_summary_hash": current_summary_hash,
        "previous_state_hash": previous_state_hash,
        "current_state_hash": current_state_hash,
        "claims_delta": diff_lists(previous_state["claims"], claims),
        "definitions_delta": diff_lists(previous_state["definitions"], definitions),
        "findings_delta": diff_lists(previous_state["findings"], findings),
    }
    delta["delta_hash"] = _sha256_obj(delta)

    out_json = os.path.join(output_root, "knowledge_delta.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(delta, f, indent=2, ensure_ascii=False)

    out_md = os.path.join(output_root, "knowledge_delta.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(
            "# Knowledge Delta\n\n"
            f"- previous_summary_hash: {delta['previous_summary_hash']}\n"
            f"- current_summary_hash: {delta['current_summary_hash']}\n"
            f"- previous_state_hash: {delta['previous_state_hash']}\n"
            f"- current_state_hash: {delta['current_state_hash']}\n"
            f"- delta_hash: {delta['delta_hash']}\n\n"
            "## Added Claims\n" +
            "\n".join(f"- {x}" for x in delta["claims_delta"]["added"]) + "\n\n" +
            "## Removed Claims\n" +
            "\n".join(f"- {x}" for x in delta["claims_delta"]["removed"]) + "\n\n" +
            "## Added Definitions\n" +
            "\n".join(f"- {x}" for x in delta["definitions_delta"]["added"]) + "\n\n" +
            "## Removed Definitions\n" +
            "\n".join(f"- {x}" for x in delta["definitions_delta"]["removed"]) + "\n\n" +
            "## Added Findings\n" +
            "\n".join(f"- {x}" for x in delta["findings_delta"]["added"]) + "\n\n" +
            "## Removed Findings\n" +
            "\n".join(f"- {x}" for x in delta["findings_delta"]["removed"]) + "\n"
        )

    existing = sorted(
        f for f in os.listdir(receipts_root)
        if f.startswith("knowledge_delta_") and f.endswith(".json")
    )
    receipt = {
        "type": "knowledge_delta",
        "timestamp": delta["timestamp"],
        "delta_hash": delta["delta_hash"],
        "previous_summary_hash": delta["previous_summary_hash"],
        "current_summary_hash": delta["current_summary_hash"],
        "output_files": [out_json, out_md]
    }
    receipt["hash"] = _sha256_obj(receipt)
    receipt_path = os.path.join(receipts_root, f"knowledge_delta_{len(existing)+1:04d}.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    index["latest_knowledge_state"] = current_state
    index["latest_knowledge_delta_hash"] = delta["delta_hash"]
    index["latest_knowledge_receipt"] = receipt_path
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    result = {
        "status": "ok",
        "delta_hash": delta["delta_hash"],
        "output_json": out_json,
        "output_md": out_md,
        "receipt_path": receipt_path,
        "index_path": INDEX_PATH
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main():
    parser = argparse.ArgumentParser(description="Track deterministic changes between canonical knowledge states.")
    parser.add_argument("--canonical-root", default=DEFAULT_CANONICAL_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--receipts-root", default=DEFAULT_RECEIPTS_ROOT)
    args = parser.parse_args()
    build_delta(
        canonical_root=args.canonical_root,
        output_root=args.output_root,
        receipts_root=args.receipts_root
    )


if __name__ == "__main__":
    main()
