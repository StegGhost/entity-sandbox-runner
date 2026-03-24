from typing import Any, Dict, List

def actuate(closure_output: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    for action in closure_output.get("actions", []):
        results.append({
            "action": action.get("action"),
            "status": "proposed_only",
            "targets": action.get("targets", []),
            "reason": action.get("reason", "")
        })

    return {
        "mode": "ingested_module",
        "summary": "Actuator preserved non-mutating proposed action list",
        "results": results
    }
