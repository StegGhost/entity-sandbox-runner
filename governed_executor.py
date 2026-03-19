from authority_resolver import AuthorityResolver
from receipt_chain_verifier import verify_chain, is_chain_locked
from decision_state_recorder import record_decision
import os

resolver = AuthorityResolver()

def execute_proposal(proposal, receipt_dir="receipts"):
    if is_chain_locked():
        return {"status": "rejected", "stage": "chain_locked"}

    check = verify_chain(receipt_dir)
    if not check["valid"]:
        return {"status": "rejected", "stage": "chain_integrity", "reason": check["reason"]}

    auth = resolver.resolve(proposal)
    if not auth.get("valid"):
        return {"status": "rejected", "stage": "authority", "reason": auth.get("reason")}

    result = proposal["execute"]()

    prev_hash = None
    if os.path.exists(receipt_dir):
        files = sorted([f for f in os.listdir(receipt_dir) if f.endswith(".json")])
        if files:
            import json
            with open(os.path.join(receipt_dir, files[-1])) as f:
                prev_hash = json.load(f).get("receipt_hash")

    receipt = record_decision(
        proposal, result, 1.0, {"action": "allow"}, auth, prev_hash, receipt_dir
    )

    return {"status": "committed", "receipt": receipt}