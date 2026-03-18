import json
import os
import random

# run ingestion first so incoming bundles get installed before evaluation
try:
    from install.ingestion_v2 import run as run_ingestion
except Exception:
    run_ingestion = None

from install.policy_engine import load_policy
from install.bcat_engine import enforce_bcat
from install.crypto_keys import sign_with_keypair, verify_chain
from install.replay import record_cycle
from install.finco import apply_finco
from install.network_registry import get_peer_receipts
from install.consensus_engine import weighted_consensus

STATE_FILE = "logs/state.json"


def load_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "cycles": 0,
        "last_hash": None
    }


def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def run_cycle():
    results = []
    for shard in ["s1", "s2", "s3"]:
        confidence = random.uniform(0.5, 0.9)
        decision = "ok" if confidence > 0.6 else "fail"
        results.append(
            {
                "shard": shard,
                "confidence": confidence,
                "decision": decision
            }
        )
    return results


def compute_u(results):
    if not results:
        return 0.0
    return sum(r["confidence"] for r in results) / len(results)


def main():
    # self-install any waiting bundles first
    if run_ingestion is not None:
        try:
            run_ingestion()
        except Exception as e:
            print("INGESTION ERROR:", str(e))

    state = load_state()
    state["cycles"] += 1

    results = run_cycle()
    u = compute_u(results)

    # Fin-Co / external pressure simulation
    external_signal = random.uniform(0.4, 0.8)
    u = apply_finco(u, external_signal)

    policy = load_policy()
    local_action, reason = enforce_bcat(policy, u)

    # peer awareness + consensus
    peer_receipts = get_peer_receipts()
    consensus_action = weighted_consensus(local_action, peer_receipts)

    receipt = {
        "cycle": state["cycles"],
        "u": u,
        "local_action": local_action,
        "consensus_action": consensus_action,
        "reason": reason,
        "external_signal": external_signal,
        "peers_seen": len(peer_receipts),
        "prev_hash": state.get("last_hash")
    }

    receipt["hash"], receipt["signature"] = sign_with_keypair(receipt)

    os.makedirs("payload/receipts", exist_ok=True)
    receipt_path = f"payload/receipts/r_{state['cycles']:04d}.json"
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    # verify chain after write
    verify_chain("payload/receipts")

    state["last_hash"] = receipt["hash"]
    save_state(state)

    record_cycle(state, results, consensus_action, u)

    print("SUMMARY:", receipt)


if __name__ == "__main__":
    main()
