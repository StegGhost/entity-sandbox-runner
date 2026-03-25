
def validate_across_nodes(result):
    # placeholder: future remote quorum check
    if not result.get("valid"):
        return result
    return {"valid": True, "nodes": ["local"], "quorum": True}
