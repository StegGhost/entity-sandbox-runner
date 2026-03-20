from typing import Any, Dict, List, Tuple


REQUIRED_PROPOSAL_FIELDS: List[str] = [
    "model_id",
    "agent_id",
    "session_id",
    "proposal_name",
    "authority_id",
    "tool_target",
    "payload",
]


class ContractValidationError(ValueError):
    pass


def validate_proposal_contract(proposal: Dict[str, Any]) -> Tuple[bool, List[str]]:
    missing = [field for field in REQUIRED_PROPOSAL_FIELDS if field not in proposal]
    return len(missing) == 0, missing


def assert_valid_proposal_contract(proposal: Dict[str, Any]) -> None:
    valid, missing = validate_proposal_contract(proposal)
    if not valid:
        raise ContractValidationError(
            f"Proposal missing required fields: {', '.join(missing)}"
        )
