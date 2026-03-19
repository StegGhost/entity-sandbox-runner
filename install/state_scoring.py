import json, os, time, hashlib

DEFAULT_CONFIG = {
    "sources": {
        "anomaly_report": "payload/anomaly_detection/anomaly_report.json",
        "preflight_report": "payload/preflight/preflight_guard_report.json",
        "priority_weights": "payload/runtime/priority_weights.json",
        "goal_execution_log": "payload/runtime/goal_execution_log.json"
    },
    "output_root": "payload/state_scoring",
    "receipts_root": "payload/receipts/state_scoring"
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

def main():
    cfg = _load_json("config/state_scoring_config.json", DEFAULT_CONFIG)
    merged = DEFAULT_CONFIG.copy()
    if isinstance(cfg, dict):
        merged.update(cfg)

    os.makedirs(merged["output_root"], exist_ok=True)
    os.makedirs(merged["receipts_root"], exist_ok=True)

    src = merged["sources"]
    anomaly = _load_json(src["anomaly_report"], {})
    preflight = _load_json(src["preflight_report"], {})
    priorities = _load_json(src["priority_weights"], {})
    goals = _load_json(src["goal_execution_log"], {})

    anomaly_count = int(anomaly.get("anomaly_count", 0))
    preflight_ok = 1 if preflight.get("status") == "ok" else 0
    priority_items = len(priorities.get("items", []))
    executed_count = sum(1 for x in goals.get("executed", []) if x.get("status") == "executed")
    skipped_count = sum(1 for x in goals.get("executed", []) if x.get("status") == "skipped")

    score = 100
    score -= anomaly_count * 15
    score += preflight_ok * 10
    score += min(priority_items, 10)
    score += min(executed_count, 10)
    score -= min(skipped_count, 10)
    score = max(0, min(100, score))

    band = "excellent" if score >= 85 else "good" if score >= 70 else "watch" if score >= 50 else "critical"

    report = {
        "timestamp": time.time(),
        "score": score,
        "band": band,
        "components": {
            "anomaly_count": anomaly_count,
            "preflight_ok": preflight_ok,
            "priority_items": priority_items,
            "executed_count": executed_count,
            "skipped_count": skipped_count
        }
    }
    report["hash"] = _sha256_obj(report)

    report_path = os.path.join(merged["output_root"], "state_score.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    md_path = os.path.join(merged["output_root"], "state_score.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(
            "# State Score\n\n"
            f"- score: {score}\n"
            f"- band: {band}\n\n"
            "## Components\n"
            f"- anomaly_count: {anomaly_count}\n"
            f"- preflight_ok: {preflight_ok}\n"
            f"- priority_items: {priority_items}\n"
            f"- executed_count: {executed_count}\n"
            f"- skipped_count: {skipped_count}\n"
        )

    existing = sorted(f for f in os.listdir(merged["receipts_root"]) if f.startswith("state_scoring_") and f.endswith(".json"))
    receipt = {
        "type": "state_scoring",
        "timestamp": report["timestamp"],
        "score": score,
        "band": band,
        "report_hash": report["hash"],
        "report_path": report_path
    }
    receipt["hash"] = _sha256_obj(receipt)
    receipt_path = os.path.join(merged["receipts_root"], f"state_scoring_{len(existing)+1:04d}.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "status": "ok",
        "score": score,
        "band": band,
        "report_path": report_path,
        "receipt_path": receipt_path
    }, indent=2))

if __name__ == "__main__":
    main()
