import json
import os
import random

from install.preflight_canonical import run_preflight
from install.receipt_guard import validate_and_repair
from install.crypto_keys import sign_with_keypair, verify_chain
from install.node_identity import get_node_id
from install.policy_engine import load_policy
from install.bcat_engine import enforce_bcat
from install.network_registry import get_peer_receipts
from install.peer_verification import verify_peer_receipt
from install.reputation_decay import decay
from install.anomaly import detect_anomaly
from install.policy_voting import vote
from install.audit import record
from install.drift import drift
from install.quorum import quorum
from install.arbitration import arbitrate

STATE = "logs/state.json"
RECEIPT_DIR = "payload/receipts"
INTEGRITY_DIR = "payload/integrity"

DEFAULT_STATE = {
    "cycles": 0,
    "u": [],
    "trust": {}
}

def load_state():
    if os.path.exists(STATE) and os.path.getsize(STATE) > 0:
        try:
            with open(STATE, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return DEFAULT_STATE.copy()
            for k, v in DEFAULT_STATE.items():
                if k not in data:
                    data[k] = v
            if not isinstance(data.get("u"), list):
                data["u"] = []
            if not isinstance(data.get("trust"), dict):
                data["trust"] = {}
            return data
        except Exception:
            pass
    return DEFAULT_STATE.copy()

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)

def save_preflight_receipt(preflight):
    os.makedirs(INTEGRITY_DIR, exist_ok=True)
    existing = sorted([f for f in os.listdir(INTEGRITY_DIR) if f.endswith(".json")])
    idx = len(existing) + 1
    path = os.path.join(INTEGRITY_DIR, f"preflight_{idx:04d}.json")
    with open(path, "w") as f:
        json.dump(preflight, f, indent=2)
    return path

def main():
    os.makedirs(RECEIPT_DIR, exist_ok=True)

    run_type = os.environ.get("RUN_TYPE", "adaptive_v20")
    preflight = run_preflight(run_type)
    preflight_path = save_preflight_receipt(preflight)
    print("PREFLIGHT:", preflight)

    if preflight.get("status") != "pass":
        raise Exception("Preflight failed — aborting")

    state = load_state()
    state["cycles"] += 1

    u = random.uniform(0.5, 0.9)
    state["u"].append(u)
    state["u"] = state["u"][-20:]

    policy = load_policy()
    local, _reason = enforce_bcat(policy, u)

    peers = [r for r in get_peer_receipts() if verify_peer_receipt(r)]

    state["trust"] = decay(state.get("trust", {}))

    actions = [local] + [p.get("consensus_action", "monitor") for p in peers]
    consensus = vote(actions) if quorum(peers) else local

    anomaly = detect_anomaly(state["u"])
    final, why = arbitrate(local, consensus, anomaly)

    receipt = {
        "node": get_node_id(),
        "cycle": state["cycles"],
        "u": u,
        "local": local,
        "consensus": consensus,
        "final": final,
        "reason": why,
        "drift": drift(state["u"]),
        "run_type": run_type,
        "preflight_status": preflight.get("status"),
        "canonical_profile_hash": preflight.get("canonical_profile_hash"),
        "preflight_receipt_path": preflight_path,
    }

    receipt["hash"], receipt["signature"] = sign_with_keypair(receipt)

    receipt_path = os.path.join(RECEIPT_DIR, f"r_{state['cycles']:04d}.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    repairs = validate_and_repair()
    if repairs:
        print("RECEIPT REPAIRS:", repairs)

    verify_chain(RECEIPT_DIR)

    record(receipt)
    save_state(state)

    print("SUMMARY:", receipt)

if __name__ == "__main__":
    main()
