from proposal_adapter import normalize_proposal
from decision_engine import decide
from governed_executor import execute_if_allowed

from policy_engine import evaluate_policy
from llm_weighting import get_score, update_score
from signature_verifier import verify_signature
from u_signal_engine import compute_u_signal
from consensus_engine import reach_consensus
from receipt_stream import emit_receipt
from external_connectors import execute_external

ENABLE_CONSENSUS = True
CONSENSUS_THRESHOLD = 2


def route_proposal(raw_input: dict):
    proposal = normalize_proposal(raw_input)

    # -------------------------
    # 🔐 Signature verification
    # -------------------------
    if "signature" in raw_input:
        if not verify_signature(proposal):
            return {"allowed": False, "reason": "invalid_signature"}

    # -------------------------
    # 🧠 Compute U signal
    # -------------------------
    context = raw_input.get("context", {})
    u_signal = compute_u_signal(proposal, context)

    # -------------------------
    # 📊 Trust score
    # -------------------------
    model_id = proposal.get("model_id", "unknown")
    score = get_score(model_id)

    # -------------------------
    # 🧾 Policy evaluation
    # -------------------------
    policy_result = evaluate_policy(proposal, u_signal, score)

    if not policy_result["allowed"]:
        update_score(model_id, False)
        return policy_result

    # -------------------------
    # ⚖️ Decision engine
    # -------------------------
    decision = decide(proposal)

    if not decision["allowed"]:
        update_score(model_id, False)
        return decision

    # -------------------------
    # 🌐 Consensus (optional)
    # -------------------------
    if policy_result.get("require_consensus") and ENABLE_CONSENSUS:
        simulated_nodes = [decision, decision]  # replace with real nodes later
        consensus = reach_consensus(simulated_nodes, CONSENSUS_THRESHOLD)

        if not consensus["allowed"]:
            return consensus

    # -------------------------
    # ⚙️ Execution
    # -------------------------
    result = execute_if_allowed(proposal, proposal.get("authority_id"))

    external = execute_external(proposal)

    update_score(model_id, True)

    emit_receipt({
        "proposal": proposal,
        "decision": decision,
        "u_signal": u_signal,
        "model_score": score,
        "result": result,
        "external": external
    })

    return {
        "decision": decision,
        "result": result,
        "u_signal": u_signal,
        "model_score": score,
        "external": external
    }
