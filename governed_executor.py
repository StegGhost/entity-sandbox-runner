from typing import Dict, Any, Optional, Callable
import os

from authority_resolver import AuthorityResolver
from predictive_engine import simulate_future_u, is_future_stable
from decision_state_recorder import record_decision
from receipt_chain import get_latest_receipt_hash
from receipt_chain_verifier import verify_chain
from u_signal_monitor import compute_u
from stability_governor import evaluate_stability

try:
    from hash_chain import append_hash
except ImportError:
    append_hash = None


resolver = AuthorityResolver()


def _normalize_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    return {"raw_result": result}


def _count_receipts(receipt_dir: str) -> int:
    if not os.path.isdir(receipt_dir):
        return 0
    return len([f for f in os.listdir(receipt_dir) if f.endswith(".json")])


def execute_proposal(
    proposal: Dict[str, Any],
    receipt_dir: str = "receipts",
) -> Dict[str, Any]:

    # 🔷 STRICT + SAFE chain verification
    chain_check = verify_chain(receipt_dir)
    receipt_count = _count_receipts(receipt_dir)

    if not chain_check.get("valid", True):
        # Only allow true bootstrap (0 or 1 receipts)
        if receipt_count > 1:
            return {
                "status": "rejected",
                "stage": "chain_integrity",
                "reason": chain_check.get("reason", "chain_invalid"),
            }

    # 🔷 Authority resolution
    auth_result = resolver.resolve(proposal)

    if not auth_result.get("valid", False):
        return {
            "status": "rejected",
            "stage": "authority",
            "reason": auth_result.get("reason", "authority_resolution_failed"),
            "authority": auth_result,
        }

    # 🔷 Predictive simulation
    future_u = simulate_future_u(proposal)

    if not is_future_stable(future_u):
        return {
            "status": "rejected",
            "stage": "predictive",
            "reason": "future_instability",
            "forecast": future_u,
        }

    # 🔷 Stability evaluation
    u_value = compute_u(proposal)
    decision = evaluate_stability(u_value)

    if decision.get("action") == "reject":
        return {
            "status": "rejected",
            "stage": "stability",
            "reason": decision.get("reason", "stability_rejection"),
            "u": u_value,
            "decision": decision,
        }

    # 🔷 Execute proposal
    execute_fn: Optional[Callable[..., Any]] = proposal.get("execute")

    if not callable(execute_fn):
        return {
            "status": "rejected",
            "stage": "execution",
            "reason": "missing_execute_callable",
        }

    try:
        raw_result = execute_fn()
        result = _normalize_result(raw_result)
    except Exception as e:
        return {
            "status": "failed",
            "stage": "execution",
            "error": str(e),
        }

    # 🔷 Chain linkage
    previous_receipt_hash = get_latest_receipt_hash(receipt_dir=receipt_dir)

    receipt = record_decision(
        proposal=proposal,
        result=result,
        u_value=u_value,
        decision=decision,
        authority=auth_result,
        previous_receipt_hash=previous_receipt_hash,
        receipt_dir=receipt_dir,
    )

    # 🔷 Optional hash chain extension
    if append_hash is not None:
        append_hash(receipt)

    return {
        "status": "committed",
        "u": u_value,
        "decision": decision,
        "forecast": future_u,
        "previous_receipt_hash": previous_receipt_hash,
        "receipt": receipt,
    }
