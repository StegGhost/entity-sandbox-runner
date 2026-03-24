def reconcile(proposal, state):
    # compare against:
    # - repo structure
    # - ingestion rules
    # - past failures
    return {
        "valid": True/False,
        "violations": [...],
        "required_changes": [...]
    }
