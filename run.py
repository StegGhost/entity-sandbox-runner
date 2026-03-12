import json
import time
import yaml
import hashlib

def compute_viability(g, c, t, K, alpha, beta, gamma):
    """Compute the maximum admissible artefact pressure given the current state."""
    return K * (g ** alpha) * (c ** beta) * (t ** gamma)

def update_state(state, delta_a):
    """Propose a new state by adjusting the artefact and degrading governance/trust."""
    g, c, a, t = state
    # degrade governance and trust slightly each step
    new_g = max(0.0, g - 0.05)
    new_c = c  # keep constraints constant in this experiment
    new_a = min(1.0, a + delta_a)
    new_t = max(0.0, t - 0.03)
    return (new_g, new_c, new_a, new_t)

def create_receipt(prev_hash, state, proposal, evaluation):
    """Create a receipt record for a state transition."""
    receipt = {
        "prev_receipt_hash": prev_hash,
        "timestamp": time.time(),
        "proposal": proposal,
        "evaluation": evaluation,
        "state": {
            "g": state[0],
            "c": state[1],
            "a": state[2],
            "t": state[3],
        },
    }
    # compute hash of the receipt for chaining
    rec_bytes = json.dumps(receipt, sort_keys=True).encode()
    rec_hash = hashlib.sha256(rec_bytes).hexdigest()
    receipt["receipt_hash"] = rec_hash
    return receipt, rec_hash

def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    g, c, a, t = config["initial_state"]
    K = float(config["K"])
    alpha = float(config["alpha"])
    beta = float(config["beta"])
    gamma = float(config["gamma"])
    steps = int(config["steps"])
    delta_a = float(config["delta_a"])

    receipts = []
    prev_hash = ""
    admissible_count = 0
    rejected_count = 0

    for step in range(steps):
        proposal = {"delta_a": delta_a}
        # propose a new state
        proposed_state = update_state((g, c, a, t), delta_a)
        # evaluate admissibility
        viability = compute_viability(proposed_state[0], proposed_state[1], proposed_state[3],
                                      K, alpha, beta, gamma)
        admissible = proposed_state[2] <= viability
        evaluation = {"viability": viability, "admissible": admissible}

        receipt, prev_hash = create_receipt(prev_hash, proposed_state, proposal, evaluation)
        receipts.append(receipt)

        if admissible:
            # accept the proposal and update current state
            g, c, a, t = proposed_state
            admissible_count += 1
        else:
            # reject: state does not change
            rejected_count += 1

    with open("receipts.json", "w") as f:
        json.dump(receipts, f, indent=2)

    print(f"Completed {steps} steps: {admissible_count} accepted, {rejected_count} rejected.")
    print("Receipts written to receipts.json")

if __name__ == "__main__":
    main()