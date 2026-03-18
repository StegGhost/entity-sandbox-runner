import json
import os
import random

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


def load():
    if os.path.exists(STATE) and os.path.getsize(STATE) > 0:
        try:
            with open(STATE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"cycles": 0, "u": [], "trust": {}}


def save(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    os.makedirs(RECEIPT_DIR, exist_ok=True)

    state = load()
    state["cycles"] += 1

    u = random.uniform(0.5, 0.9)
    state["u"].append(u)
    state["u"] = state["u"][-20:]

    policy = load_policy()
    local, reason = enforce_bcat(policy, u)

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
    save(state)

    print("SUMMARY:", receipt)


if __name__ == "__main__":
    main()
