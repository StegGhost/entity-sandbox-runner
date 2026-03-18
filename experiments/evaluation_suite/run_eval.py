import json
import os
import random

from install.check_file_engine import run_integrity_check
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


# 🔧 HARD GUARANTEE STATE SCHEMA
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

            # enforce schema every run
            for k, v in DEFAULT_STATE.items():
                if k not in data:
                    data[k] = v

            if not isinstance(data.get("u"), list):
                data["u"] = []

            if not isinstance(data.get("trust"), dict):
                data["trust"] = {}

            return data
        except:
            pass

    return DEFAULT_STATE.copy()


def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    os.makedirs(RECEIPT_DIR, exist_ok=True)

    # 🔐 INTEGRITY FIRST
    integrity = run_integrity_check()
    print("INTEGRITY:", integrity.get("status"))

    if integrity.get("status") == "fail":
        raise Exception("Integrity failed — aborting")

    # 🔄 LOAD STATE (SELF-HEALING)
    s = load_state()

    # 🔁 CYCLE
    s["cycles"] += 1

    u = random.uniform(0.5, 0.9)

    # 🔧 GUARANTEED SAFE APPEND
    if "u" not in s or not isinstance(s["u"], list):
        s["u"] = []

    s["u"].append(u)
    s["u"] = s["u"][-20:]

    # 🔐 POLICY
    policy = load_policy()
    local, reason = enforce_bcat(policy, u)

    # 🌐 PEERS
    peers = [r for r in get_peer_receipts() if verify_peer_receipt(r)]

    # 🔁 TRUST DECAY
    s["trust"] = decay(s.get("trust", {}))

    # 🗳 CONSENSUS
    actions = [local] + [p.get("consensus_action", "monitor") for p in peers]
    consensus = vote(actions) if quorum(peers) else local

    # 🚨 ANOMALY
    anomaly = detect_anomaly(s["u"])

    # ⚖️ FINAL DECISION
    final, why = arbitrate(local, consensus, anomaly)

    # 🧾 RECEIPT
    receipt = {
        "node": get_node_id(),
        "cycle": s["cycles"],
        "u": u,
        "local": local,
        "consensus": consensus,
        "final": final,
        "reason": why,
        "drift": drift(s["u"]),
        "integrity_status": integrity.get("status"),
        "integrity_hash": integrity.get("repo_integrity_hash")
    }

    receipt["hash"], receipt["signature"] = sign_with_keypair(receipt)

    path = os.path.join(RECEIPT_DIR, f"r_{s['cycles']:04d}.json")
    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    # 🧹 REPAIR + VERIFY
    repairs = validate_and_repair()
    if repairs:
        print("RECEIPT REPAIRS:", repairs)

    verify_chain(RECEIPT_DIR)

    # 📝 AUDIT + SAVE
    record(receipt)
    save_state(s)

    print("SUMMARY:", receipt)


if __name__ == "__main__":
    main()
