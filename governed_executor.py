from u_signal_monitor import compute_u
from stability_governor import evaluate_stability
from decision_state_recorder import record_decision
from hash_chain import append_hash
from authority_resolver import AuthorityResolver

resolver = AuthorityResolver()

def execute_proposal(proposal):
    # 0. Resolve authority
    auth_result = resolver.resolve(proposal)

    if not auth_result["valid"]:
        return {
            "status": "rejected",
            "reason": auth_result["reason"]
        }

    # 1. Compute U
    u_value = compute_u(proposal)

    # 2. Stability decision
    decision = evaluate_stability(u_value)

    if decision["action"] == "reject":
        return {
            "status": "rejected",
            "reason": decision["reason"],
            "u": u_value
        }

    # 3. Execute
    result = proposal["execute"]()

    # 4. Record
    receipt = record_decision(
        proposal=proposal,
        result=result,
        u_value=u_value,
        decision=decision,
        authority=auth_result
    )

    # 5. Chain
    append_hash(receipt)

    return {
        "status": "committed",
        "u": u_value,
        "receipt": receipt
    }
