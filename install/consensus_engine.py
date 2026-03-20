def reach_consensus(results: list, threshold: int = 2) -> dict:
    approvals = sum(1 for r in results if r.get("allowed"))

    if approvals >= threshold:
        return {"allowed": True, "approvals": approvals}

    return {"allowed": False, "reason": "consensus_failed"}
