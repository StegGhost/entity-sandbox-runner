from u_signal_monitor import compute_u
from stability_governor import evaluate_stability
from decision_state_recorder import record_decision
from hash_chain import append_hash

def execute_proposal(proposal):
    # 1. Evaluate U
    u_value = compute_u(proposal)

    # 2. Governance decision
    decision = evaluate_stability(u_value)

    if decision["action"] == "reject":
        return {
            "status": "rejected",
            "reason": decision["reason"],
            "u": u_value
        }

    # 3. Commit
    result = proposal["execute"]()

    # 4. Record decision
    receipt = record_decision(
        proposal=proposal,
        result=result,
        u_value=u_value,
        decision=decision
    )

    # 5. Chain it
    append_hash(receipt)

    return {
        "status": "committed",
        "u": u_value,
        "receipt": receipt
    }
