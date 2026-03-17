
import json, os, random

STATE_FILE = "logs/state.json"
AVAILABLE_WORKERS = ["w1","w2","w3"]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "workers": {}, "mode": "normal", "failures": [], "anomalies": []}

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def compute_u(history):
    if not history:
        return 0.5
    recent = history[-10:]
    return sum(h["confidence"] for h in recent) / len(recent)

def score_worker(state, worker, confidence):
    w = state["workers"].setdefault(worker, {"score": 0.5, "count": 0})
    w["score"] = (w["score"] * w["count"] + confidence) / (w["count"] + 1)
    w["count"] += 1

def classify(u):
    if u > 0.75:
        return "stable", "allow"
    elif u > 0.6:
        return "warning", "monitor"
    return "critical", "restrict"

def detect_anomaly(state, u):
    prev = state.get("last_u")
    state["last_u"] = u
    if prev is None:
        return False
    if abs(u - prev) > 0.2:
        state.setdefault("anomalies", []).append({"prev": prev, "current": u})
        return True
    return False

def prune_state(state):
    state["history"] = state["history"][-50:]
    state["failures"] = state.get("failures", [])[-20:]
    state["anomalies"] = state.get("anomalies", [])[-20:]

def select_worker(state):
    workers = state.get("workers", {})
    for w in AVAILABLE_WORKERS:
        workers.setdefault(w, {"score": 0.5, "count": 0})
    if random.random() < 0.2:
        return random.choice(AVAILABLE_WORKERS)
    return max(workers.items(), key=lambda x: x[1]["score"])[0]

def external_signal():
    return random.uniform(0.0, 1.0)

def enforce_policy(state, action):
    if state.get("mode") == "conservative" and action == "allow":
        return "monitor"
    if len(state.get("failures", [])) > 10:
        return "restrict"
    return action

def control_response(u, state):
    if u < 0.6:
        state["mode"] = "conservative"
    elif u > 0.8:
        state["mode"] = "aggressive"
    else:
        state["mode"] = "normal"

def reassign_if_failed(state, result):
    if result["decision"] == "fail":
        state.setdefault("failures", []).append({
            "shard": result["shard"],
            "confidence": result["confidence"]
        })
        return "w_fallback"
    return result["worker"]

def run_cycle(state):
    shards = ["shard1","shard2","shard3"]
    if state.get("mode") == "conservative":
        shards = shards[:2]
    elif state.get("mode") == "aggressive":
        shards = shards + ["shard4","shard5"]

    out = []
    for s in shards:
        worker = select_worker(state)
        c = random.uniform(0.5, 0.9)
        d = "ok" if c > 0.6 else "fail"
        out.append({"worker":worker,"shard":s,"confidence":c,"decision":d})
    return out

def main():
    state = load_state()
    results = run_cycle(state)

    for r in results:
        r["worker"] = reassign_if_failed(state, r)
        state["history"].append({"confidence": r["confidence"], "decision": r["decision"]})
        score_worker(state, r["worker"], r["confidence"])

    u = compute_u(state["history"])
    ext = external_signal()
    u = (u * 0.7) + (ext * 0.3)

    anomaly = detect_anomaly(state, u)

    system_state, action = classify(u)
    action = enforce_policy(state, action)

    control_response(u, state)
    prune_state(state)

    summary = {
        "u_signal": u,
        "state": system_state,
        "action": action,
        "mode": state.get("mode"),
        "anomaly": anomaly,
        "workers": state.get("workers")
    }

    print("RESULTS:", results)
    print("SUMMARY:", summary)

    save_state(state)

if __name__ == "__main__":
    main()
