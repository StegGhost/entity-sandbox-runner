import os
import json
import time
import hashlib
import inspect

from state_reconstructor import reconstruct_state


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
            return {"valid": False, "reason": "unknown_authority"}

        return {
            "valid": True,
            "authority_id": authority_id,
            "authority": self.authorities[authority_id]
        }


resolver = AuthorityResolver()


def hash_data(data):
    encoded = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def compute_execution_fingerprint(proposal):
    try:
        source = inspect.getsource(proposal["execute"])
    except Exception:
        source = str(proposal["execute"])

    payload = {
        "proposal_name": proposal["name"],
        "authority_id": proposal["authority_id"],
        "code": source,
    }

    return hash_data(payload)


def execute_proposal(proposal, receipt_dir="receipts"):
    os.makedirs(receipt_dir, exist_ok=True)

    authority = resolver.resolve(proposal["authority_id"])
    if not authority["valid"]:
        return {
            "status": "rejected",
            "stage": "authority",
            "reason": authority["reason"]
        }

    # 🔥 STATE BEFORE
    state_before = reconstruct_state(receipt_dir, strict=False)
    state_before_hash = hash_data(state_before)

    try:
        result = proposal["execute"]()
    except Exception as e:
        return {
            "status": "rejected",
            "stage": "execution",
            "reason": str(e)
        }

    # 🔥 STATE AFTER
    state_after = dict(state_before)
    state_after[proposal["name"]] = result
    state_after_hash = hash_data(state_after)

    files = sorted(os.listdir(receipt_dir))
    prev_hash = None

    if files:
        last_path = os.path.join(receipt_dir, files[-1])
        with open(last_path, "r") as f:
            prev = json.load(f)
            prev_hash = prev.get("receipt_hash")

    receipt = {
        "schema_version": "3.0.0",
        "timestamp": time.time(),
        "proposal": proposal["name"],
        "result": result,
        "authority": authority,
        "previous_receipt_hash": prev_hash,

        # 🔥 NEW CORE FIELDS
        "state_before_hash": state_before_hash,
        "state_after_hash": state_after_hash,
        "execution_fingerprint": compute_execution_fingerprint(proposal)
    }

    receipt["receipt_hash"] = hash_data(receipt)

    filename = f"{int(time.time())}_{receipt['receipt_hash'][:10]}.json"
    path = os.path.join(receipt_dir, filename)

    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    return {
        "status": "committed",
        "receipt": receipt,
        "receipt_path": path
    }
