import json, os, random, time

from install.deterministic_enforcer import enforce_policy
from install.receipt_logger import write_receipt
from install.economic_weighting import weighted_score, weighted_mode
from install.external_signal_adapter import external_signal
from install.coordination import select_worker, reassign_if_failed, initialize_workers

STATE_FILE = "logs/state.json"
RECEIPT_DIR = "payload/receipts"
STATE_VERSION = 2

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {"version": 1, "history": [], "workers": {}, "mode": "normal", "failures": [], "anomalies": [], "last_u": None, "last_action": None, "cycles": 0}
    state = migrate_state(state)
    initialize_workers(state)
    return state

def migrate_state(state):
    version = state.get("version", 1)
    if version < 2:
        for w in state.get("workers", {}).values():
            w.setdefault("failures", 0)
        state["version"] = 2
    return state

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def prune_state(state):
    state["history"] = state.get("history", [])[-100:]
    state["failures"] = state.get("failures", [])[-50:]
    state["anomalies"] = state.get("anomalies", [])[-50:]

def classify(u):
    if u >= 0.80:
        return "stable", "allow"
    if u >= 0.62:
        return "warning", "monitor"
    return "critical", "restrict"

def detect_anomaly(state, u):
    prev = state.get("last_u")
    state["last_u"] = u
    if prev is None:
        return False
    if abs(u - prev) > 0.20:
        state.setdefault("anomalies", []).append({"prev": prev, "current": u, "ts": time.time()})
        return True
    return False

def score_worker(state, worker, confidence, decision):
    workers = state.setdefault("workers", {})
    w = workers.setdefault(worker, {"score": 0.5, "count": 0, "failures": 0})
    w.setdefault("failures", 0)

    base = confidence if decision == "ok" else max(0.0, confidence - 0.25)
    w["score"] = ((w["score"] * w["count"]) + base) / (w["count"] + 1)
    w["count"] += 1

    if decision != "ok":
        w["failures"] += 1

def run_cycle(state):
    shards = ["shard1", "shard2", "shard3"]
    if state.get("mode") == "conservative":
        shards = shards[:2]
    elif state.get("mode") == "aggressive":
        shards = shards + ["shard4","shard5"]

    results = []
    for shard in shards:
        worker = select_worker(state)
        confidence = random.uniform(0.5, 0.92)
        ext = external_signal()
        final_conf = round((confidence * 0.75) + (ext * 0.25), 6)
        decision = "ok" if final_conf > 0.6 else "fail"

        result = {"worker": worker, "shard": shard, "confidence": final_conf, "decision": decision}
        result["worker"] = reassign_if_failed(state, result)
        results.append(result)

    return results

def main():
    state = load_state()
    state["cycles"] = state.get("cycles", 0) + 1

    results = run_cycle(state)

    for r in results:
        state["history"].append(r)
        score_worker(state, r["worker"], r["confidence"], r["decision"])

    u = weighted_score(state)
    anomaly = detect_anomaly(state, u)

    proposed_state, proposed_action = classify(u)
    enforced_action, policy_reason = enforce_policy(state, proposed_action, proposed_state, u)

    state["mode"] = weighted_mode(state, u, enforced_action)
    state["last_action"] = enforced_action

    prune_state(state)
    save_state(state)

    receipt = write_receipt(RECEIPT_DIR, state, results, {"u_signal": u, "action": enforced_action})

    print("RESULTS:", results)
    print("SUMMARY:", {"u_signal": u, "action": enforced_action, "mode": state["mode"], "receipt": receipt})

if __name__ == "__main__":
    main()
