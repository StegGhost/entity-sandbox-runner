import os
import json
import time
import uuid
import inspect
from typing import Any, Dict, Optional, Tuple

from receipt_chain_verifier import verify_chain, load_receipts, build_chain, compute_hash
from state_reconstructor import reconstruct_state


class AuthorityResolver:
    def __init__(self) -> None:
        self.authorities: Dict[str, Dict[str, Any]] = {}

    def register_authority(self, authority_id: str, role: str, trust_score: float = 1.0) -> None:
        self.authorities[authority_id] = {
            "role": role,
            "trust_score": trust_score,
            "created_at": time.time(),
        }

    def resolve(self, authority_id: str) -> Dict[str, Any]:
        if authority_id not in self.authorities:
            return {"valid": False}

        return {
            "valid": True,
            "authority_id": authority_id,
            "authority": self.authorities[authority_id],
        }


resolver = AuthorityResolver()


def _compute_execution_fingerprint(proposal: Dict[str, Any]) -> str:
    execute_fn = proposal.get("execute")

    try:
        source = inspect.getsource(execute_fn)
    except Exception:
        source = repr(execute_fn)

    payload = {
        "proposal_name": proposal.get("name"),
        "authority_id": proposal.get("authority_id"),
        "execute_source": source,
    }
    return compute_hash(payload)


def _get_chain_tip(receipt_dir: str) -> Tuple[Optional[str], Optional[str]]:
    receipts = load_receipts(receipt_dir)
    if not receipts:
        return None, None

    ordered = build_chain(receipts)
    tip = ordered[-1]

    return tip.get("receipt_hash"), tip.get("process_hash")


def execute_proposal(proposal: Dict[str, Any], receipt_dir: str = "receipts") -> Dict[str, Any]:
    os.makedirs(receipt_dir, exist_ok=True)

    chain_result = verify_chain(receipt_dir)
    if chain_result.get("status") != "ok":
        return {
            "status": "rejected",
            "stage": "chain_integrity",
            "reason": chain_result.get("reason"),
        }

    authority_id = proposal.get("authority_id")
    authority = resolver.resolve(authority_id)

    if not authority.get("valid"):
        return {
            "status": "rejected",
            "stage": "authority",
            "reason": "invalid authority",
        }

    state_before = reconstruct_state(receipt_dir, strict=True)

    try:
        result = proposal["execute"]()
    except Exception as e:
        return {
            "status": "rejected",
            "stage": "execution",
            "reason": str(e),
        }

    state_after = dict(state_before)
    if isinstance(result, dict):
        state_after.update(result)

    previous_receipt_hash, previous_process_hash = _get_chain_tip(receipt_dir)

    execution_fingerprint = _compute_execution_fingerprint(proposal)

    receipt = {
        "schema_version": "4.0.0",
        "timestamp": time.time(),
        "proposal": proposal["name"],
        "result": result,
        "authority": authority,
        "previous_receipt_hash": previous_receipt_hash,
        "state_before_hash": compute_hash(state_before),
        "state_after_hash": compute_hash(state_after),
        "execution_fingerprint": execution_fingerprint,
    }

    receipt_hash = compute_hash(receipt)
    receipt["receipt_hash"] = receipt_hash

    process_material = {
        "previous_process_hash": previous_process_hash,
        "receipt_hash": receipt_hash,
        "execution_fingerprint": execution_fingerprint,
    }
    receipt["process_hash"] = compute_hash(process_material)

    filename = f"{time.time_ns()}_{receipt_hash[:8]}_{uuid.uuid4().hex[:6]}.json"
    path = os.path.join(receipt_dir, filename)
    tmp_path = path + ".tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)

    os.replace(tmp_path, path)

    return {
        "status": "committed",
        "receipt": receipt,
        "receipt_path": path,
    }
