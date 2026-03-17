# eval_metrics.py (patched for shared state)

from install.system_state import METRICS

def record(m):
    METRICS.append(m)

def summary():
    ok = sum(1 for m in METRICS if m.get("decision", {}).get("decision") == "ok")
    total = len(METRICS)
    return {
        "count": total,
        "ok": ok,
        "ok_rate": (ok / total) if total else 0.0
    }
