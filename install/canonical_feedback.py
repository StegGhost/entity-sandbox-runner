import argparse
import hashlib
import json
import os
import re
import time

RULES_PATH = "config/canonical_feedback_rules.json"
DEFAULT_CANONICAL_ROOT = "docs/canonical"
DEFAULT_OUTPUT_ROOT = "payload/feedback"
DEFAULT_RECEIPTS_ROOT = "payload/receipts/canonical_feedback"

DEFAULT_RULES = {
    "max_priority_items": 15,
    "priority_keywords": [
        "invariant",
        "deterministic",
        "receipt",
        "policy",
        "execution",
        "feedback",
        "canonical",
        "proof",
        "replay",
        "uncertainty",
        "trust",
        "constraint"
    ],
    "contradiction_markers": [
        "however",
        "but",
        "conflict",
        "contradiction",
        "inconsistent",
        "failed",
        "failure",
        "broke",
        "restrict",
        "halt"
    ]
}


def _norm(path):
    return path.replace("\\", "/")


def _sha256_obj(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()


def _load_json(path, default):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        return data
    except Exception:
        return default


def _read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def _load_rules():
    data = _load_json(RULES_PATH, {})
    if not isinstance(data, dict):
        data = {}
    merged = DEFAULT_RULES.copy()
    merged.update(data)
    return merged


def _ensure_dirs(output_root, receipts_root):
    os.makedirs(output_root, exist_ok=True)
    os.makedirs(receipts_root, exist_ok=True)


def _extract_ranked_items(md_text):
    items = []
    for line in md_text.splitlines():
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            items.append(m.group(1).strip())
            continue
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m:
            items.append(m.group(1).strip())
    return items


def _score_item(text, rules):
    score = 0
    lower = text.lower()
    for kw in rules.get("priority_keywords", []):
        if kw.lower() in lower:
            score += 3
    score += min(len(text) // 50, 4)
    return score


def _find_contradictions(items, rules):
    out = []
    markers = [m.lower() for m in rules.get("contradiction_markers", [])]
    for item in items:
        lower = item.lower()
        if any(marker in lower for marker in markers):
            out.append(item)
    return out


def build_feedback(canonical_root=DEFAULT_CANONICAL_ROOT, output_root=DEFAULT_OUTPUT_ROOT, receipts_root=DEFAULT_RECEIPTS_ROOT):
    _ensure_dirs(output_root, receipts_root)
    rules = _load_rules()

    claims_md = _read_text(os.path.join(canonical_root, "claims_canonical.md"))
    defs_md = _read_text(os.path.join(canonical_root, "definitions_canonical.md"))
    findings_md = _read_text(os.path.join(canonical_root, "findings_canonical.md"))
    summary_json = _load_json(os.path.join(canonical_root, "compaction_summary.json"), {})
    system_summary_md = _read_text(os.path.join(canonical_root, "system_summary.md"))

    claims = _extract_ranked_items(claims_md)
    definitions = _extract_ranked_items(defs_md)
    findings = _extract_ranked_items(findings_md)
    summary_items = _extract_ranked_items(system_summary_md)

    all_items = claims + definitions + findings + summary_items

    prioritized = sorted(
        list(dict.fromkeys(all_items)),
        key=lambda x: _score_item(x, rules),
        reverse=True
    )[: int(rules.get("max_priority_items", 15))]

    contradictions = _find_contradictions(all_items, rules)

    invariant_candidates = []
    for item in prioritized:
        lower = item.lower()
        if any(k in lower for k in ["invariant", "deterministic", "receipt", "policy", "replay", "uncertainty", "trust", "constraint"]):
            invariant_candidates.append(item)

    feedback = {
        "timestamp": time.time(),
        "canonical_root": _norm(canonical_root),
        "claims_count": len(claims),
        "definitions_count": len(definitions),
        "findings_count": len(findings),
        "summary_hash": summary_json.get("summary_hash"),
        "priority_items": prioritized,
        "invariant_candidates": invariant_candidates,
        "contradictions": contradictions,
        "recommended_next_actions": [
            "Feed invariant_candidates into formal document generation.",
            "Bind summary_hash into future receipts.",
            "Track delta between previous and current canonical summaries.",
            "Review contradictions before auto-promotion into policy."
        ]
    }
    feedback["hash"] = _sha256_obj(feedback)

    feedback_path = os.path.join(output_root, "canonical_feedback.json")
    with open(feedback_path, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=2, ensure_ascii=False)

    md_lines = [
        "# Canonical Feedback",
        "",
        f"- summary_hash: {feedback.get('summary_hash')}",
        f"- claims_count: {feedback.get('claims_count')}",
        f"- definitions_count: {feedback.get('definitions_count')}",
        f"- findings_count: {feedback.get('findings_count')}",
        f"- feedback_hash: {feedback.get('hash')}",
        "",
        "## Priority Items"
    ]
    for item in feedback["priority_items"]:
        md_lines.append(f"- {item}")
    md_lines.append("")
    md_lines.append("## Invariant Candidates")
    for item in feedback["invariant_candidates"]:
        md_lines.append(f"- {item}")
    md_lines.append("")
    md_lines.append("## Contradictions")
    if feedback["contradictions"]:
        for item in feedback["contradictions"]:
            md_lines.append(f"- {item}")
    else:
        md_lines.append("- none detected by current marker rules")
    md_lines.append("")
    md_lines.append("## Recommended Next Actions")
    for item in feedback["recommended_next_actions"]:
        md_lines.append(f"- {item}")

    feedback_md_path = os.path.join(output_root, "canonical_feedback.md")
    with open(feedback_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    existing = sorted(
        f for f in os.listdir(receipts_root)
        if f.startswith("canonical_feedback_") and f.endswith(".json")
    )
    receipt = {
        "type": "canonical_feedback",
        "timestamp": feedback["timestamp"],
        "summary_hash": feedback.get("summary_hash"),
        "feedback_hash": feedback["hash"],
        "input_files": [
            _norm(os.path.join(canonical_root, "claims_canonical.md")),
            _norm(os.path.join(canonical_root, "definitions_canonical.md")),
            _norm(os.path.join(canonical_root, "findings_canonical.md")),
            _norm(os.path.join(canonical_root, "compaction_summary.json")),
            _norm(os.path.join(canonical_root, "system_summary.md"))
        ],
        "output_files": [
            _norm(feedback_path),
            _norm(feedback_md_path)
        ]
    }
    receipt["hash"] = _sha256_obj(receipt)
    receipt_path = os.path.join(receipts_root, f"canonical_feedback_{len(existing)+1:04d}.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    result = {
        "status": "ok",
        "summary_hash": feedback.get("summary_hash"),
        "feedback_hash": feedback["hash"],
        "feedback_path": _norm(feedback_path),
        "receipt_path": _norm(receipt_path)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main():
    parser = argparse.ArgumentParser(description="Build structured feedback from canonical note compaction outputs.")
    parser.add_argument("--canonical-root", default=DEFAULT_CANONICAL_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--receipts-root", default=DEFAULT_RECEIPTS_ROOT)
    args = parser.parse_args()
    build_feedback(
        canonical_root=args.canonical_root,
        output_root=args.output_root,
        receipts_root=args.receipts_root
    )


if __name__ == "__main__":
    main()
