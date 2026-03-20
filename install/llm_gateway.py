from typing import Dict, Any

from decision_engine import execute_if_allowed
from proposal_adapter import normalize_proposal
from governed_executor import resolver


def route_proposal(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize incoming request (LLM / API / external)
    proposal = normalize_proposal(raw_input)

    authority_id = proposal.get("authority_id")
    authority = resolver.resolve(authority_id)

    # Route into decision + governed execution
    result = execute_if_allowed(
        proposal=proposal,
        authority=authority,
    )

    return {
        "status": "routed",
        "input": raw_input,
        "normalized": proposal,
        "result": result,
    }
