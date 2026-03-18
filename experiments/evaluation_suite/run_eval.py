import os
import json
import random

# =========================
# SAFE IMPORTS (no hard crash)
# =========================
def safe_import(path, name):
    try:
        module = __import__(path, fromlist=[name])
        return getattr(module, name)
    except Exception:
        return None

# core systems
run_repo_integrity_check = safe_import("install.check_file_engine", "run_repo_integrity_check")
bootstrap_all = safe_import("install.check_file_engine", "bootstrap_all")
validate_and_repair = safe_import("install.receipt_guard", "validate_and_repair")

get_node_id = safe_import("install.node_identity", "get_node_id")
load_policy = safe_import("install.policy_engine", "load_policy")
enforce_bcat = safe_import("install.bcat_engine", "enforce_bcat")

sign_with_keypair = safe_import("install.crypto_keys", "sign_with_keypair")

get_peer_receipts = safe_import("install.network_registry", "get_peer_receipts")
verify_peer_receipt = safe_import("install.peer_verification", "verify_peer_receipt")

decay = safe_import("install.reputation_decay", "decay")
detect_anomaly = safe_import("install.anomaly", "detect_anomaly")
vote = safe_import("install.policy_voting", "vote")
record = safe_import("install.audit", "record")
drift = safe_import("install.drift", "drift")
quorum = safe_import("install.quorum", "quorum")
arbitrate = safe_import("install.arbitration", "arbitrate")

STATE_PATH = "logs/state.json"

# =========================
# SAFE STATE HANDLING
# =========================
def load_state():
    if not os.path.exists(STATE_PATH):
        return {"cycles": 0, "u": [], "trust": {}}

    try:
        with open(STATE_PATH, "r") as f:
            data = json.load(f)
    except Exception:
        return {"cycles": 0, "u": [], "trust": {}}

    # repair missing keys
    if "cycles" not in data:
        data["cycles"] = 0
    if "u" not in data:
        data["u"] = []
    if "trust" not in data:
        data["trust"] = {}

    return data


def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


# =========================
# DEFAULT FALLBACKS
# =========================
def default_policy():
    return {
        "hard_min_u": 0.6,
        "hard_stop_u": 0.4
    }


def safe_policy():
    if load_policy:
        try:
            p = load_policy()
            if not isinstance(p, dict):
                return default_policy()
            if "hard_min_u" not in p:
                p["hard_min_u"] = 0.6
            if "hard_stop_u" not in p:
                p["hard_stop_u"] = 0.4
            return p
        except Exception:
            return default_policy()
    return default_policy()


def safe_enforce(policy, u):
    if enforce_bcat:
        try:
            return enforce_bcat(policy, u)
        except Exception:
            return "monitor", "fallback"
    return "monitor", "no_engine"


def safe_node():
    if get_node_id:
        try:
            return get_node_id()
        except Exception:
            pass
    return "node_local"


def safe_sign(receipt):
    if sign_with_keypair:
        try:
            return sign_with_keypair(receipt)
        except Exception:
            pass
    return "nohash", "nosig"


# =========================
# MAIN
# =========================
def main():

    # =========================
    # INTEGRITY CHECK + BOOTSTRAP
    # =========================
    integrity = {"status": "unknown"}

    if run_repo_integrity_check:
        try:
            integrity = run_repo_integrity_check()
            print("INTEGRITY:", integrity)
        except Exception as e:
            print("INTEGRITY ERROR:", str(e))

    if integrity.get("status") == "fail":
        print("INTEGRITY FAIL → BOOTSTRAP ATTEMPT")

        if bootstrap_all:
            try:
                result = bootstrap_all()
                print("BOOTSTRAP RESULT:", result)
            except Exception as e:
                print("BOOTSTRAP ERROR:", str(e))

        # retry integrity
        if run_repo_integrity_check:
            try:
                integrity = run_repo_integrity_check()
                print("POST-BOOTSTRAP INTEGRITY:", integrity)
            except Exception as e:
                print("RECHECK ERROR:", str(e))

        if integrity.get("status") == "fail":
            raise Exception("Integrity failed after bootstrap — aborting")

    # =========================
    # STATE
    # =========================
    state = load_state()
    state["cycles"] += 1

    # =========================
    # SIGNAL
    # =========================
    u = random.uniform(0.5, 0.9)
    state["u"].append(u)
    state["u"] = state["u"][-20:]

    # =========================
    # POLICY
    # =========================
    policy = safe_policy()
    local_action, local_reason = safe_enforce(policy, u)

    # =========================
    # PEERS
    # =========================
    peers = []
    if get_peer_receipts and verify_peer_receipt:
        try:
            raw = get_peer_receipts()
            peers = [r for r in raw if verify_peer_receipt(r)]
        except Exception:
            peers = []

    # =========================
    # TRUST DECAY
    # =========================
    if decay:
        try:
            state["trust"] = decay(state.get("trust", {}))
        except Exception:
            pass

    # =========================
    # CONSENSUS
    # =========================
    actions = [local_action] + [p.get("consensus_action", "monitor") for p in peers]

    if quorum and vote:
        try:
            consensus = vote(actions) if quorum(peers) else local_action
        except Exception:
            consensus = local_action
    else:
        consensus = local_action

    # =========================
    # ANOMALY
    # =========================
    anomaly = False
    if detect_anomaly:
        try:
            anomaly = detect_anomaly(state["u"])
        except Exception:
            pass

    # =========================
    # ARBITRATION
    # =========================
    if arbitrate:
        try:
            final, why = arbitrate(local_action, consensus, anomaly)
        except Exception:
            final, why = local_action, "fallback"
    else:
        final, why = local_action, "no_arbitration"

    # =========================
    # RECEIPT
    # =========================
    receipt = {
        "node": safe_node(),
        "cycle": state["cycles"],
        "u": u,
        "local": local_action,
        "consensus": consensus,
        "final": final,
        "reason": why
    }

    h, sig = safe_sign(receipt)
    receipt["hash"] = h
    receipt["signature"] = sig

    # =========================
    # SAVE RECEIPT
    # =========================
    os.makedirs("payload/receipts", exist_ok=True)
    path = f"payload/receipts/r_{state['cycles']:04d}.json"

    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    # optional repair pass
    if validate_and_repair:
        try:
            validate_and_repair("payload/receipts")
        except Exception:
            pass

    # audit
    if record:
        try:
            record(receipt)
        except Exception:
            pass

    save_state(state)

    print("SUMMARY:", receipt)


# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    main()
