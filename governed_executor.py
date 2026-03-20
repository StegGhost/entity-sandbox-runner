import os
import json
import time
import hashlib
import uuid

from state_reconstructor import reconstruct_state
from receipt_chain_verifier import verify_chain


class AuthorityResolver:
    def __init__(self):
        self.authorities = {}

    def register_authority(self, authority_id, role, trust_score=1.0):
        self.authorities[authority_id] = {
            "role": role,
            "trust_score": trust_score,
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


def _get_chain_tip(receipt_dir):
    receipts = []

    for fname in os.listdir(receipt_dir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(receipt_dir, fname), "r") as f:
            receipts.append(json.load(f))

    if not receipts:
        return None, None

    all_hashes = {r["receipt_hash"] for r in receipts}
    referenced = {
        r["previous_receipt_hash"]
        for r in receipts
        if r["previous_receipt_hash"] is not None
    }

    tips = list(all_hashes - referenced)

    if len(tips) != 1:
        raise Exception("Invalid chain: multiple or zero tips")

    tip_hash = tips[0]

    tip_receipt = next(r for r in receipts if r["receipt_hash"] == tip_hash)

    return tip_hash, tip_receipt.get("process_hash")


def execute_proposal(proposal, receipt_dir="receipts"):
    os.makedirs(receipt_dir, exist_ok=True)

    # HARD BLOCK: chain must be valid
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

    state_before = reconstruct_state(receipt_dir, strict=True)

    result = proposal["execute"]()

    state_after = dict(state_before)
    if isinstance(result, dict):
        state_after.update(result)

    previous_hash, previous_process_hash = _get_chain_tip(receipt_dir)

    receipt = {
        "schema_version": "4.0.0",
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

    # 🔥 NEW: process hash chain
    process_material = {
        "previous_process_hash": previous_process_hash,
        "receipt_hash": receipt_hash,
        "execution_fingerprint": receipt["execution_fingerprint"]
    }

    receipt["process_hash"] = compute_hash(process_material)

    filename = f"{time.time_ns()}_{receipt_hash[:8]}_{uuid.uuid4().hex[:6]}.json"
    path = os.path.join(receipt_dir, filename)

    with open(path, "w") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)

    return {
        "status": "committed",
        "receipt": receipt,
        "receipt_path": path
    }
