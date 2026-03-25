from typing import Any, Dict, List

from proposal_adapter import normalize_proposal
from tool_contracts import assert_valid_proposal_contract
from decision_engine import decide, execute_if_allowed


class AuthorityResolver:
    def resolve(self, authority_id: str) -> Dict[str, Any]:
        return {
            "authority_id": authority_id,
            "valid": True,
            "permissions": ["*"],
        }


resolver = AuthorityResolver()


def _build_executable_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
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
    proposal = normalize_proposal(raw_input)

    try:
        assert_valid_proposal_contract(proposal)
    except Exception as e:
        return {
            "allowed": False,
            "reason": "contract_violation",
            "error": str(e),
        }

    proposal = _build_executable_proposal(proposal)

    authority = resolver.resolve(proposal.get("authority_id"))

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


# 🔥 PRIMARY ENTRYPOINT
def route_proposal(input_data: Any) -> Dict[str, Any]:
    if isinstance(input_data, list):
        return {
            "results": [_evaluate_single(item) for item in input_data]
        }

    return _evaluate_single(input_data)


# 🔥 BACKWARD COMPATIBILITY FIX (THIS IS YOUR ERROR FIX)
def route_multi_proposal(input_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Required by:
    - api_server.py
    - test_api.py
    - test_llm_adapter.py

    This restores old interface while using new engine.
    """
    return {
        "results": [_evaluate_single(item) for item in input_list]
    }
