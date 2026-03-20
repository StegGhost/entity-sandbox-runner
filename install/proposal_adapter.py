def normalize_proposal(raw: dict) -> dict:
    return {
        "name": raw.get("proposal_name") or raw.get("name"),
        "authority_id": raw.get("authority_id"),
        "payload": raw.get("payload", {}),
        "model_id": raw.get("model_id", "unknown"),
        "confidence": raw.get("confidence", 1.0),
        "justification": raw.get("justification", "")
    }
