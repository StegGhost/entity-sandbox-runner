from typing import Any, Dict

from agent_registry import AgentRegistry
from proposal_adapter import ProposalAdapter


class LLMGateway:
    def __init__(self, registry: AgentRegistry, adapter: ProposalAdapter) -> None:
        self.registry = registry
        self.adapter = adapter

    def prepare_proposal(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        proposal = self.adapter.normalize(raw_input)

        agent = self.registry.get_agent(proposal["agent_id"])
        if not agent:
            raise ValueError("Unknown agent_id")

        if agent["model_id"] != proposal["model_id"]:
            raise ValueError("model_id does not match registered agent")

        if not self.registry.is_tool_allowed(proposal["agent_id"], proposal["tool_target"]):
            raise ValueError("tool_target not allowed for agent")

        return {
            "name": proposal["proposal_name"],
            "authority_id": proposal["authority_id"],
            "payload": proposal["payload"],
            "metadata": {
                "model_id": proposal["model_id"],
                "agent_id": proposal["agent_id"],
                "session_id": proposal["session_id"],
                "tool_target": proposal["tool_target"],
                "justification": proposal.get("justification", ""),
                "confidence": proposal.get("confidence", 0.0),
                "state_claims": proposal.get("state_claims", {}),
            },
        }
