from llm_adapter import LLMAdapter


def main() -> None:
    adapter = LLMAdapter()

    adapter.register_agent(
        agent_id="agent_ops",
        model_id="gpt-5.x",
        role="ops",
        authority_id="local_admin",
        allowed_tools=["records.update"],
        trust_score=1.0,
    )

    raw_input = {
        "model_id": "gpt-5.x",
        "agent_id": "agent_ops",
        "session_id": "session-123",
        "proposal_name": "update_customer_record",
        "authority_id": "local_admin",
        "tool_target": "records.update",
        "payload": {"customer_id": "123", "status": "active"},
        "justification": "Authorized status correction.",
        "confidence": 0.92,
        "state_claims": {"expected_record_exists": True},
    }

    proposal = adapter.adapt(raw_input)

    assert proposal["name"] == "update_customer_record"
    assert proposal["authority_id"] == "local_admin"
    assert proposal["payload"]["status"] == "active"
    assert proposal["metadata"]["agent_id"] == "agent_ops"

    print("LLM adapter test successful.")


if __name__ == "__main__":
    main()
