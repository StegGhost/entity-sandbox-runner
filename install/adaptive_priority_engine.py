import json, os, time, hashlib

DEFAULT = {
  "input_path": "payload/runtime/active_feedback.json",
  "output_path": "payload/runtime/priority_weights.json",
  "receipts_root": "payload/receipts/adaptive_priority",
  "weights": {
    "contradictions": 3.0,
    "invariant_candidates": 2.0,
    "priority_items": 1.5,
    "recommended_next_actions": 1.0
  },
  "top_k": 20
}

def _load(p, d):
    try:
        if not os.path.exists(p): return d
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except Exception:
        return d

def _sha(o):
    raw = json.dumps(o, sort_keys=True, ensure_ascii=False).encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()

def score_items(data, w):
    scored = []
    for k, weight in w.items():
        items = data.get(k, []) or []
        for it in items:
            text = it if isinstance(it, str) else json.dumps(it, ensure_ascii=False)
            score = weight
            scored.append({"category": k, "item": it, "score": score, "text": text})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

def main():
    cfg = _load("config/adaptive_priority_config.json", DEFAULT)
    merged = DEFAULT.copy(); merged.update(cfg)

    data = _load(merged["input_path"], {})
    os.makedirs(os.path.dirname(merged["output_path"]), exist_ok=True)
    os.makedirs(merged["receipts_root"], exist_ok=True)

    scored = score_items(data, merged["weights"])
    top = scored[: merged.get("top_k", 20)]

    out = {
        "timestamp": time.time(),
        "top_k": len(top),
        "items": top
    }

    with open(merged["output_path"], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # receipt
    existing = [f for f in os.listdir(merged["receipts_root"]) if f.startswith("adaptive_priority_")]
    rec = {"type":"adaptive_priority","timestamp":out["timestamp"],"output_path":merged["output_path"]}
    rec["hash"] = _sha(rec)
    rp = os.path.join(merged["receipts_root"], f"adaptive_priority_{len(existing)+1:04d}.json")
    with open(rp, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2)

    print(json.dumps({"status":"ok","output":merged["output_path"],"receipt":rp}, indent=2))

if __name__ == "__main__":
    main()
