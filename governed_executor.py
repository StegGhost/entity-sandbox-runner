from typing import Dict, Any, Optional, Callable

from receipt_chain_verifier import verify_chain
from authority_resolver import AuthorityResolver
from predictive_engine import simulate_future_u, is_future_stable
from decision_state_recorder import record_decision
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

# 🔷 0. Verify chain integrity before doing anything
chain_ok, message = verify_chain()

if not chain_ok:
    return {
        "status": "rejected",
        "stage": "chain_integrity",
        "reason": message
    }
    
def execute_proposal(
    proposal: Dict[str, Any],
    previous_receipt_hash: Optional[str] = None,
    receipt_dir: str = "receipts",
) -> Dict[str, Any]:
    auth_result = resolver.resolve(proposal)

    if not auth_result.get("valid", False):
        return {
            "status": "rejected",
            "stage": "authority",
            "reason": auth_result.get("reason", "authority_resolution_failed"),
            "authority": auth_result,
        }

    future_u = simulate_future_u(proposal)

    if not is_future_stable(future_u):
        return {
            "status": "rejected",
            "stage": "predictive",
            "reason": "future_instability",
            "forecast": future_u,
        }

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

    receipt = record_decision(
        proposal=proposal,
        result=result,
        u_value=u_value,
        decision=decision,
        authority=auth_result,
        previous_receipt_hash=previous_receipt_hash,
        receipt_dir=receipt_dir,
    )

    if append_hash is not None:
        append_hash(receipt)

    return {
        "status": "committed",
        "u": u_value,
        "decision": decision,
        "forecast": future_u,
        "receipt": receipt,
    }
