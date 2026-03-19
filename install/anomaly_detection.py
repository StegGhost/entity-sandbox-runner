import json, os, time, hashlib

DEFAULT_CONFIG = {
    "receipts_roots": [
        "payload/receipts/document_compaction",
        "payload/receipts/canonical_feedback",
        "payload/receipts/knowledge_delta",
        "payload/receipts/canonical_state",
        "payload/receipts/feedback_injection",
        "payload/receipts/feedback_execution_bridge",
        "payload/receipts/actuator_bridge"
    ],
    "output_root": "payload/anomaly_detection",
    "receipts_root": "payload/receipts/anomaly_detection",
    "warn_if_missing_root": False
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

def _latest_json(root):
    if not os.path.exists(root):
        return None, None
    files = sorted(f for f in os.listdir(root) if f.endswith(".json"))
    if not files:
        return None, None
    path = os.path.join(root, files[-1])
    return path, _load_json(path, {})

def main():
    cfg = _load_json("config/anomaly_detection_config.json", DEFAULT_CONFIG)
    merged = DEFAULT_CONFIG.copy()
    if isinstance(cfg, dict):
        merged.update(cfg)

    os.makedirs(merged["output_root"], exist_ok=True)
    os.makedirs(merged["receipts_root"], exist_ok=True)

    roots = merged.get("receipts_roots", [])
    details = []
    anomalies = []

    for root in roots:
        path, data = _latest_json(root)
        exists = os.path.exists(root)
        files = sorted(os.listdir(root)) if exists else []
        detail = {
            "root": root,
            "exists": exists,
            "file_count": len(files),
            "latest_path": path,
            "latest_type": data.get("type") if isinstance(data, dict) else None,
            "latest_status": data.get("status") if isinstance(data, dict) else None
        }
        details.append(detail)

        if not exists and merged.get("warn_if_missing_root", False):
            anomalies.append({"root": root, "kind": "missing_root"})
        elif exists and len(files) == 0:
            anomalies.append({"root": root, "kind": "empty_root"})
        elif isinstance(data, dict) and data.get("status") in ("failed", "blocked", "fail"):
            anomalies.append({"root": root, "kind": "bad_latest_status", "status": data.get("status")})

    report = {
        "timestamp": time.time(),
        "status": "warn" if anomalies else "ok",
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "details": details
    }
    report["hash"] = _sha256_obj(report)

    report_path = os.path.join(merged["output_root"], "anomaly_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    md_path = os.path.join(merged["output_root"], "anomaly_report.md")
    lines = [
        "# Anomaly Detection Report",
        "",
        f"- status: {report['status']}",
        f"- anomaly_count: {report['anomaly_count']}",
        ""
    ]
    if anomalies:
        lines.append("## Anomalies")
        for a in anomalies:
            lines.append(f"- {a}")
        lines.append("")
    lines.append("## Receipt Roots")
    for d in details:
        lines.append(f"- {d['root']} | exists={d['exists']} | file_count={d['file_count']} | latest_status={d['latest_status']}")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    existing = sorted(f for f in os.listdir(merged["receipts_root"]) if f.startswith("anomaly_detection_") and f.endswith(".json"))
    receipt = {
        "type": "anomaly_detection",
        "timestamp": report["timestamp"],
        "status": report["status"],
        "report_hash": report["hash"],
        "report_path": report_path
    }
    receipt["hash"] = _sha256_obj(receipt)
    receipt_path = os.path.join(merged["receipts_root"], f"anomaly_detection_{len(existing)+1:04d}.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "status": report["status"],
        "report_path": report_path,
        "receipt_path": receipt_path
    }, indent=2))

if __name__ == "__main__":
    main()
