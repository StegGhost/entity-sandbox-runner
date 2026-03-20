import os
import json
import time
import hashlib

from state_reconstructor import reconstruct_state
from receipt_chain_verifier import verify_chain


class AuthorityResolver:
    def __init__(self):
        self.authorities = {}

    def register_authority(self, authority_id, role):
        self.authorities[authority_id] = {
            "role": role,
            "trust_score": 1.0,
            "created_at": time.time()
        }

    def resolve(self, authority_id):
        if authority_id not in self.authorities:
            return {"valid": False}

        return {
            "valid": True,
            "authority_id": authority_id,
            "authority": self.authorities[authority_id]
        }


resolver = AuthorityResolver()


def compute_hash(data):
    encoded = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def execute_proposal(proposal, receipt_dir="receipts"):
    os.makedirs(receipt_dir, exist_ok=True)

    # 🔴 CRITICAL FIX: enforce chain BEFORE anything else
    chain_result = verify_chain(receipt_dir)
    if chain_result["status"] != "ok":
        return {
            "status": "rejected",
            "stage": "chain_integrity",
            "reason": chain_result["reason"]
        }

    authority = resolver.resolve(proposal["authority_id"])

    if not authority["valid"]:
        return {
            "status": "rejected",
            "stage": "authority",
            "reason": "invalid authority"
        }

    # reconstruct valid state
    state_before = reconstruct_state(receipt_dir, strict=True)

    result = proposal["execute"]()

    state_after = dict(state_before)
    if isinstance(result, dict):
        state_after.update(result)

    previous_hash = None
    files = sorted(os.listdir(receipt_dir))
    if files:
        last_file = files[-1]
        with open(os.path.join(receipt_dir, last_file), "r") as f:
            previous_receipt = json.load(f)
            previous_hash = previous_receipt.get("receipt_hash")

    receipt = {
        "schema_version": "3.0.0",
        "timestamp": time.time(),
        "proposal": proposal["name"],
        "result": result,
        "authority": authority,
        "previous_receipt_hash": previous_hash,
        "state_before_hash": compute_hash(state_before),
        "state_after_hash": compute_hash(state_after),
        "execution_fingerprint": compute_hash(proposal["name"]),
    }

    receipt_hash = compute_hash(receipt)
    receipt["receipt_hash"] = receipt_hash

    filename = f"{int(receipt['timestamp'])}_{receipt_hash[:8]}.json"
    path = os.path.join(receipt_dir, filename)

    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    return {
        "status": "committed",
        "receipt": receipt,
        "receipt_path": path
    }
