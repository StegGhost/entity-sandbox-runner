from typing import Any, Dict, Optional


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, Dict[str, Any]] = {}

    def register_agent(
        self,
        agent_id: str,
        model_id: str,
        role: str,
        authority_id: str,
        allowed_tools: Optional[list] = None,
        trust_score: float = 1.0,
    ) -> None:
        self._agents[agent_id] = {
            "agent_id": agent_id,
            "model_id": model_id,
            "role": role,
            "authority_id": authority_id,
            "allowed_tools": allowed_tools or [],
            "trust_score": trust_score,
        }

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        return self._agents.get(agent_id)

    def is_tool_allowed(self, agent_id: str, tool_target: str) -> bool:
        agent = self.get_agent(agent_id)
        if not agent:
            return False
        allowed = agent.get("allowed_tools", [])
        return not allowed or tool_target in allowed
