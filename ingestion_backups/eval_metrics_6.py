# eval_metrics.py

metrics = []

def record(m):
    metrics.append(m)

def summary():
    ok = sum(1 for m in metrics if m.get("decision", {}).get("decision") == "ok")
    total = len(metrics)
    return {
        "count": total,
        "ok": ok,
        "ok_rate": (ok / total) if total else 0.0
    }
