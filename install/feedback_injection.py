import argparse
import hashlib
import json
import os
import time

DEFAULT_CONFIG = {
    "feedback_path": "payload/feedback/canonical_feedback.json",
    "injection_root": "payload/injection",
    "receipts_root": "payload/receipts/feedback_injection",
    "max_invariant_candidates": 10,
    "max_priority_items": 10,
    "max_contradictions": 10
}


def _norm(path):
    return path.replace("\\\\", "/")


def _load_json(path, default):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return default


def _sha256_obj(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()


def build_injection(config):
    feedback = _load_json(config.get("feedback_path"), {})
    injection_root = config.get("injection_root", "payload/injection")
    receipts_root = config.get("receipts_root", "payload/receipts/feedback_injection")

    os.makedirs(injection_root, exist_ok=True)
    os.makedirs(receipts_root, exist_ok=True)

    priority_items = feedback.get("priority_items", [])[: int(config.get("max_priority_items", 10))]
    invariant_candidates = feedback.get("invariant_candidates", [])[: int(config.get("max_invariant_candidates", 10))]
    contradictions = feedback.get("contradictions", [])[: int(config.get("max_contradictions", 10))]
    recommended = feedback.get("recommended_next_actions", [])

    prompt_inputs = {
        "summary_hash": feedback.get("summary_hash"),
        "feedback_hash": feedback.get("hash"),
        "priority_items": priority_items,
        "invariant_candidates": invariant_candidates,
        "contradictions": contradictions,
        "recommended_next_actions": recommended
    }

    prompt_path = os.path.join(injection_root, "feedback_prompt_inputs.json")
    with open(prompt_path, "w", encoding="utf-8") as f:
        json.dump(prompt_inputs, f, indent=2, ensure_ascii=False)

    md_lines = [
        "# Feedback Injection Inputs",
        "",
        f"- summary_hash: {feedback.get('summary_hash')}",
        f"- feedback_hash: {feedback.get('hash')}",
        "",
        "## Priority Items"
    ]
    for item in priority_items:
        md_lines.append(f"- {item}")
    md_lines.append("")
    md_lines.append("## Invariant Candidates")
    for item in invariant_candidates:
        md_lines.append(f"- {item}")
    md_lines.append("")
    md_lines.append("## Contradictions")
    if contradictions:
        for item in contradictions:
            md_lines.append(f"- {item}")
    else:
        md_lines.append("- none")
    md_lines.append("")
    md_lines.append("## Recommended Next Actions")
    for item in recommended:
        md_lines.append(f"- {item}")

    md_path = os.path.join(injection_root, "feedback_prompt_inputs.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\\n".join(md_lines))

    policy_inputs = {
        "invariant_candidates": invariant_candidates,
        "contradictions": contradictions,
        "priority_items": priority_items
    }
    policy_path = os.path.join(injection_root, "feedback_policy_inputs.json")
    with open(policy_path, "w", encoding="utf-8") as f:
        json.dump(policy_inputs, f, indent=2, ensure_ascii=False)

    receipt = {
        "type": "feedback_injection",
        "timestamp": time.time(),
        "summary_hash": feedback.get("summary_hash"),
        "feedback_hash": feedback.get("hash"),
        "output_files": [
            _norm(prompt_path),
            _norm(md_path),
            _norm(policy_path)
        ]
    }
    receipt["hash"] = _sha256_obj(receipt)

    existing = sorted(
        f for f in os.listdir(receipts_root)
        if f.startswith("feedback_injection_") and f.endswith(".json")
    )
    receipt_path = os.path.join(receipts_root, f"feedback_injection_{len(existing)+1:04d}.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    result = {
        "status": "ok",
        "feedback_hash": feedback.get("hash"),
        "receipt_path": _norm(receipt_path),
        "prompt_inputs": _norm(prompt_path),
        "policy_inputs": _norm(policy_path)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main():
    parser = argparse.ArgumentParser(description="Inject canonical feedback into reusable prompt and policy inputs.")
    parser.add_argument("--config", default="config/feedback_injection_config.json")
    args = parser.parse_args()
    cfg = _load_json(args.config, DEFAULT_CONFIG.copy())
    merged = DEFAULT_CONFIG.copy()
    if isinstance(cfg, dict):
        merged.update(cfg)
    build_injection(merged)


if __name__ == "__main__":
    main()
