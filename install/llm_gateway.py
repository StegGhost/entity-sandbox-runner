from typing import Any, Dict, List

from proposal_adapter import normalize_proposal
from tool_contracts import assert_valid_proposal_contract
from decision_engine import decide, execute_if_allowed


class AuthorityResolver:
    def resolve(self, authority_id: str) -> Dict[str, Any]:
        # Minimal deterministic authority model
        return {
            "authority_id": authority_id,
            "valid": True,
            "permissions": ["*"],
        }


resolver = AuthorityResolver()


def _build_executable_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures proposal has executable surface.
    """

    if not callable(proposal.get("execute")):
        payload = proposal.get("payload", {})
        name = proposal.get("proposal_name", "unnamed")

        def _execute():
            return {
                "ok": True,
                "proposal": name,
                "payload": payload,
            }

        proposal["execute"] = _execute

    return proposal


def _evaluate_single(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    # STEP 1: Normalize
    proposal = normalize_proposal(raw_input)

    # STEP 2: HARD CONTRACT VALIDATION
    try:
        assert_valid_proposal_contract(proposal)
    except Exception as e:
        return {
            "allowed": False,
            "reason": "contract_violation",
            "error": str(e),
        }

    # STEP 3: Make executable
    proposal = _build_executable_proposal(proposal)

    # STEP 4: Resolve authority
    authority = resolver.resolve(proposal.get("authority_id"))

    # STEP 5: Decision
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

    # STEP 6: Execution
    result = execute_if_allowed(
        proposal=proposal,
        authority=authority,
    )

    return {
        "decision": decision,
        "result": result,
    }


def route_proposal(input_data: Any) -> Dict[str, Any]:
    """
    Entry point for ALL LLM proposals.
    Supports single or batch input.
    """

    if isinstance(input_data, list):
        return {
            "results": [_evaluate_single(item) for item in input_data]
        }

    return _evaluate_single(input_data)
