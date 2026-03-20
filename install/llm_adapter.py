from typing import Any, Dict

from agent_registry import AgentRegistry
from llm_gateway import LLMGateway
from proposal_adapter import ProposalAdapter


class LLMAdapter:
    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self.registry = registry or AgentRegistry()
        self.adapter = ProposalAdapter()
        self.gateway = LLMGateway(self.registry, self.adapter)

    def register_agent(
        self,
        agent_id: str,
        model_id: str,
        role: str,
        authority_id: str,
        allowed_tools: list | None = None,
        trust_score: float = 1.0,
    ) -> None:
        self.registry.register_agent(
            agent_id=agent_id,
            model_id=model_id,
            role=role,
            authority_id=authority_id,
            allowed_tools=allowed_tools,
            trust_score=trust_score,
        )

    def adapt(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        return self.gateway.prepare_proposal(raw_input)
