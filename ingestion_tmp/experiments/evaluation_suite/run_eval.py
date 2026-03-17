
import json, os, random

STATE_FILE = "logs/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "workers": {}}

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

def run_cycle():
    shards = ["shard1","shard2","shard3"]
    out = []
    for s in shards:
        c = random.uniform(0.5, 0.9)
        d = "ok" if c > 0.6 else "fail"
        out.append({"worker":"w1","shard":s,"confidence":c,"decision":d})
    return out

def main():
    state = load_state()
    results = run_cycle()

    for r in results:
        state["history"].append({"confidence": r["confidence"], "decision": r["decision"]})
        score_worker(state, r["worker"], r["confidence"])

    u = compute_u(state["history"])
    system_state, action = classify(u)

    summary = {"u_signal": u, "state": system_state, "action": action}

    print("RESULTS:", results)
    print("SUMMARY:", summary)

    save_state(state)

if __name__ == "__main__":
    main()
