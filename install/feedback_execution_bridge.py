import json
import os
import time
import hashlib

DEFAULT_CONFIG = {
    "feedback_input": "payload/injection/feedback_prompt_inputs.json",
    "output_root": "payload/runtime",
    "engine_input_path": "payload/runtime/active_feedback.json",
    "receipts_root": "payload/receipts/feedback_execution_bridge"
}


def _load_json(path, default):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _sha256_obj(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()


def run_bridge(config):
    feedback = _load_json(config["feedback_input"], {})

    os.makedirs(config["output_root"], exist_ok=True)
    os.makedirs(config["receipts_root"], exist_ok=True)

    # Normalize structure for engines
    engine_input = {
        "timestamp": time.time(),
        "summary_hash": feedback.get("summary_hash"),
        "feedback_hash": feedback.get("feedback_hash"),
        "priority_items": feedback.get("priority_items", []),
        "invariant_candidates": feedback.get("invariant_candidates", []),
        "contradictions": feedback.get("contradictions", []),
        "recommended_next_actions": feedback.get("recommended_next_actions", [])
    }

    # Write active input
    with open(config["engine_input_path"], "w", encoding="utf-8") as f:
        json.dump(engine_input, f, indent=2, ensure_ascii=False)

    # Build receipt
    receipt = {
        "type": "feedback_execution_bridge",
        "timestamp": engine_input["timestamp"],
        "feedback_hash": engine_input["feedback_hash"],
        "summary_hash": engine_input["summary_hash"],
        "engine_input_path": config["engine_input_path"]
    }
    receipt["hash"] = _sha256_obj(receipt)

    existing = sorted(
        f for f in os.listdir(config["receipts_root"])
        if f.startswith("feedback_execution_bridge_") and f.endswith(".json")
    )
    receipt_path = os.path.join(
        config["receipts_root"],
        f"feedback_execution_bridge_{len(existing)+1:04d}.json"
    )

    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    result = {
        "status": "ok",
        "engine_input_path": config["engine_input_path"],
        "receipt_path": receipt_path
    }

    print(json.dumps(result, indent=2))
    return result


def main():
    cfg = _load_json("config/feedback_execution_bridge_config.json", DEFAULT_CONFIG)
    merged = DEFAULT_CONFIG.copy()
    merged.update(cfg)
    run_bridge(merged)


if __name__ == "__main__":
    main()
