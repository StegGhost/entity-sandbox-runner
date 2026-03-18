import json
import os
import random
from install.policy_engine import load_policy
from install.bcat_engine import enforce_bcat
from install.crypto_keys import sign_with_keypair, verify_chain
from install.replay import record_cycle

STATE_FILE = "logs/state.json"

def load_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"cycles": 0, "last_hash": None}

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def run_cycle():
    results = []
    for s in ["s1", "s2", "s3"]:
        c = random.uniform(0.5, 0.9)
        d = "ok" if c > 0.6 else "fail"
        results.append({"shard": s, "confidence": c, "decision": d})
    return results

def compute_u(results):
    return sum(x["confidence"] for x in results) / len(results)

def main():
    state = load_state()
    state["cycles"] += 1

    results = run_cycle()
    u = compute_u(results)

    policy = load_policy()
    action, reason = enforce_bcat(policy, u)

    receipt = {
        "cycle": state["cycles"],
        "u": u,
        "action": action,
        "reason": reason,
        "prev_hash": state.get("last_hash")
    }

    receipt["hash"], receipt["signature"] = sign_with_keypair(receipt)

    os.makedirs("payload/receipts", exist_ok=True)
    path = f"payload/receipts/r_{state['cycles']:04d}.json"
    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    verify_chain("payload/receipts")

    state["last_hash"] = receipt["hash"]
    save_state(state)

    record_cycle(state, results, action, u)

    print("SUMMARY:", receipt)

if __name__ == "__main__":
    main()
