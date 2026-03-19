import os
import json
from typing import List, Dict, Any


def _load_receipts(receipt_dir: str) -> List[Dict[str, Any]]:
    if not os.path.isdir(receipt_dir):
        return []

    files = sorted(
        [f for f in os.listdir(receipt_dir) if f.endswith(".json")]
    )

    receipts = []

    for f in files:
        path = os.path.join(receipt_dir, f)
        with open(path, "r", encoding="utf-8") as file:
            receipts.append(json.load(file))

    return receipts


def reconstruct_state(receipt_dir: str = "receipts") -> Dict[str, Any]:
    receipts = _load_receipts(receipt_dir)

    state = {
        "total_executions": 0,
        "last_u": None,
        "last_decision": None,
        "authorities": [],
        "authority_history": [],
        "authority_drift_detected": False,
        "history": [],
    }

    seen_authorities = []
    last_authority_id = None

    for r in receipts:
        state["total_executions"] += 1

        state["last_u"] = r.get("u_value")
        state["last_decision"] = r.get("decision")

        authority = r.get("authority", {})
        authority_id = authority.get("authority_id")

        if authority_id and authority_id not in seen_authorities:
            seen_authorities.append(authority_id)

        state["authority_history"].append({
            "timestamp": r.get("timestamp"),
            "proposal": r.get("proposal"),
            "authority_id": authority_id,
        })

        if last_authority_id is not None and authority_id != last_authority_id:
            state["authority_drift_detected"] = True

        last_authority_id = authority_id

        state["history"].append({
            "proposal": r.get("proposal"),
            "u": r.get("u_value"),
            "decision": r.get("decision"),
            "timestamp": r.get("timestamp"),
            "authority_id": authority_id,
        })

    state["authorities"] = seen_authorities
    return state


def print_state_summary(state: Dict[str, Any]):
    print("\n=== RECONSTRUCTED SYSTEM STATE ===")
    print(f"Total Executions: {state['total_executions']}")
    print(f"Last U: {state['last_u']}")
    print(f"Last Decision: {state['last_decision']}")
    print(f"Authorities: {state['authorities']}")
    print(f"Authority Drift Detected: {state['authority_drift_detected']}")
    print("=================================\n")
