from proposal_adapter import normalize_proposal
from decision_engine import decide
from governed_executor import execute_if_allowed
from policy_engine import get_policy
from llm_weighting import get_score, update_score
from receipt_stream import emit_receipt
from external_connectors import execute_external
from policy_engine import evaluate_policy
from llm_weighting import get_score

def route_proposal(raw_input: dict):
    proposal = normalize_proposal(raw_input)

    model_id = proposal.get("model_id", "unknown")
    score = get_score(model_id)

    # ---- U signal (placeholder for now) ----
    u_signal = raw_input.get("u_signal", 1.0)

    policy_result = evaluate_policy(proposal, u_signal, score)

    if not policy_result["allowed"]:
        return policy_result

    decision = decide(proposal)

    if not decision["allowed"]:
        return decision
ENABLE_CONSENSUS = False

def route_proposal(raw_input: dict):
    proposal = normalize_proposal(raw_input)

    model_id = proposal.get("model_id", "unknown")
    score = get_score(model_id)

    policy = get_policy(proposal)

    # ---- Trust check ----
    if score < policy["min_trust"]:
        return {"allowed": False, "reason": "low_trust_model"}

    decision = decide(proposal)

    if not decision["allowed"]:
        update_score(model_id, False)
        return decision

    # ---- Execution ----
    result = execute_if_allowed(proposal, proposal.get("authority_id"))

    # ---- External routing ----
    external = execute_external(proposal)

    # ---- Update trust ----
    update_score(model_id, True)

    # ---- Emit receipt ----
    emit_receipt({
        "proposal": proposal,
        "decision": decision,
        "result": result,
        "external": external
    })

    return {
        "decision": decision,
        "result": result,
        "external": external,
        "model_score": get_score(model_id)
    }
