import random
from proposal_adapter import normalize_proposal
from agent_registry import get_agent
from decision_engine import decide
from governed_executor import execute_if_allowed

ENABLE_MULTI_LLM = True
ENABLE_CONSENSUS = False  # toggle Path B
CONSENSUS_THRESHOLD = 2

def route_proposal(raw_input: dict):
    proposal = normalize_proposal(raw_input)

    # ---- Path A: Multi-LLM simulation ----
    if ENABLE_MULTI_LLM and "variants" in raw_input:
        results = []
        for variant in raw_input["variants"]:
            p = normalize_proposal(variant)
            decision = decide(p)
            results.append(decision)

        if ENABLE_CONSENSUS:
            approvals = sum(1 for r in results if r["allowed"])
            if approvals < CONSENSUS_THRESHOLD:
                return {"allowed": False, "reason": "consensus_failed"}

        return results[0]

    # ---- Single proposal path ----
    decision = decide(proposal)

    if not decision["allowed"]:
        return decision

    # ---- Path D: Execute ----
    result = execute_if_allowed(proposal, proposal.get("authority_id"))

    return {
        "decision": decision,
        "result": result
    }
