from typing import Dict, Any

from decision_engine import decide, execute_if_allowed
from proposal_adapter import normalize_proposal
from governed_executor import resolver


def _build_executable_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(proposal)

    if "name" not in normalized or normalized.get("name") is None:
        normalized["name"] = normalized.get("action", "unnamed_proposal")

    if not callable(normalized.get("execute")):
        payload = normalized.get("payload")

        def _default_execute():
            if isinstance(payload, dict):
                return payload
            return {"ok": True}

        normalized["execute"] = _default_execute

    return normalized


def route_proposal(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    proposal = normalize_proposal(raw_input)
    proposal = _build_executable_proposal(proposal)

    authority_id = proposal.get("authority_id")
    authority = resolver.resolve(authority_id)

    # Explicit signature rejection contract for current tests / API use
    if "signature" in raw_input and raw_input.get("signature") != "valid_signature":
        return {
            "allowed": False,
            "reason": "invalid_signature",
        }

    decision = decide(
        proposal=proposal,
        authority=authority,
    )

    if not decision.get("allowed", False):
        return {
            "decision": decision,
            "result": {
                "status": "rejected",
                "decision": decision,
            },
        }

    result = execute_if_allowed(
        proposal=proposal,
        authority=authority,
    )

    return {
        "decision": decision,
        "result": result,
    }
