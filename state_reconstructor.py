import os
import json
from typing import List, Dict, Any


RECEIPT_DIR = "receipts"


def _load_receipts(receipt_dir=RECEIPT_DIR) -> List[Dict[str, Any]]:
    if not os.path.isdir(receipt_dir):
        return []

    files = sorted([
        f for f in os.listdir(receipt_dir)
        if f.endswith(".json")
    ])

    receipts = []

    for f in files:
        path = os.path.join(receipt_dir, f)
        with open(path, "r", encoding="utf-8") as file:
            receipts.append(json.load(file))

    return receipts


def reconstruct_state(receipt_dir):
    receipts = load_receipts(receipt_dir)

    total_executions = 0
    last_u = None
    last_decision = None
    authorities = set()

    for r in receipts:
        total_executions += 1

        receipt = r.get("receipt", {})

        last_u = receipt.get("u_value", last_u)
        last_decision = receipt.get("decision", last_decision)

        # 🔷 NEW: extract authority
        auth = receipt.get("authority", {})
        authority_id = receipt.get("authority_id")

        if authority_id:
            authorities.add(authority_id)

    return {
        "total_executions": total_executions,
        "last_u": last_u,
        "last_decision": last_decision,
        "authorities": sorted(list(authorities)),  # 🔷 FIX
    }

def print_state_summary(state: Dict[str, Any]):
    print("\n=== RECONSTRUCTED SYSTEM STATE ===")
    print(f"Total Executions: {state['total_executions']}")
    print(f"Last U: {state['last_u']}")
    print(f"Last Decision: {state['last_decision']}")
    print(f"Authorities: {list(state['authority_map'].keys())}")
    print("=================================\n")
