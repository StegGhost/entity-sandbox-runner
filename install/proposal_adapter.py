from typing import Any, Dict

from tool_contracts import assert_valid_proposal_contract


class ProposalAdapter:
    def normalize(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        proposal = {
            "model_id": raw_input.get("model_id"),
            "agent_id": raw_input.get("agent_id"),
            "session_id": raw_input.get("session_id"),
            "proposal_name": raw_input.get("proposal_name"),
            "authority_id": raw_input.get("authority_id"),
            "tool_target": raw_input.get("tool_target"),
            "payload": raw_input.get("payload", {}),
            "justification": raw_input.get("justification", ""),
            "confidence": raw_input.get("confidence", 0.0),
            "state_claims": raw_input.get("state_claims", {}),
        }
        assert_valid_proposal_contract(proposal)
        return proposal
