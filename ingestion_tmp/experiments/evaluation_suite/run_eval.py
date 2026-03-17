
import json, os, time, random

STATE_FILE = "logs/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"history": []}

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def compute_u_signal(history):
    if not history:
        return 0.5
    recent = history[-5:]
    return sum([h["confidence"] for h in recent]) / len(recent)

def run_cycle():
    shards = ["shard1", "shard2", "shard3"]
    results = []
    for s in shards:
        confidence = random.uniform(0.5, 0.9)
        decision = "ok" if confidence > 0.6 else "fail"
        results.append({
            "assignment": {"worker": "w1", "shard": s},
            "decision": {"decision": decision, "confidence": confidence}
        })
    return results

def main():
    state = load_state()
    results = run_cycle()

    for r in results:
        state["history"].append({
            "confidence": r["decision"]["confidence"],
            "decision": r["decision"]["decision"]
        })

    u = compute_u_signal(state["history"])

    if u > 0.75:
        system_state = "stable"
        action = "allow"
    elif u > 0.6:
        system_state = "warning"
        action = "monitor"
    else:
        system_state = "critical"
        action = "restrict"

    summary = {
        "u_signal": u,
        "state": system_state,
        "action": action,
        "count": len(results)
    }

    print("RESULTS:", results)
    print("SUMMARY:", summary)

    save_state(state)

if __name__ == "__main__":
    main()
