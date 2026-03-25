from typing import Any, Dict, Optional, List

from agent_registry import AgentRegistry
from llm_gateway import route_proposal


class LLMAdapter:
    """
    Controlled LLM execution surface.

    Responsibilities:
    - Register agents
    - Accept raw or state-driven inputs
    - Route through governed execution
    """

    def __init__(self, registry: Optional[AgentRegistry] = None) -> None:
        self.registry = registry or AgentRegistry()

    def register_agent(
        self,
        agent_id: str,
        model_id: str,
        role: str,
        authority_id: str,
        allowed_tools: Optional[List[str]] = None,
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
        """
        Direct proposal execution.
        """
        return route_proposal(raw_input)

    def observe_and_propose(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        STATE-AWARE ENTRYPOINT

        observation example:
        {
            "goal": "...",
            "state": {...},
            "failures": [...],
            "next_actions": [...]
        }
        """

        proposal = {
            "proposal_name": "state_driven_action",
            "authority_id": "system",
            "tool_target": "repo",
            "payload": observation,
            "model_id": "llm",
            "agent_id": "observer",
            "session_id": "runtime",
        }

        return route_proposal(proposal)
