def normalize_proposal(raw: dict) -> dict:
    return {
        # REQUIRED CONTRACT FIELDS
        "model_id": raw.get("model_id", "unknown"),
        "agent_id": raw.get("agent_id", "default_agent"),
        "session_id": raw.get("session_id", "default_session"),
        "proposal_name": raw.get("proposal_name") or raw.get("name"),
        "authority_id": raw.get("authority_id"),
        "tool_target": raw.get("tool_target", "repo"),
        "payload": raw.get("payload", {}),

        # OPTIONAL / EXTENDED
        "confidence": raw.get("confidence", 1.0),
        "justification": raw.get("justification", ""),
    }
