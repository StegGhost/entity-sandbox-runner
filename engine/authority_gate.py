
from engine.authority_policy import validate_paths

def run_authority_gate(manifest: dict):
    result = validate_paths(manifest)
    if not result.get("valid"):
        return {
            "valid": False,
            "reason": result.get("reason"),
            "violations": result.get("violations", [])
        }
    return {"valid": True}
