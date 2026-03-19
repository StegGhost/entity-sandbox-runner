from typing import Dict, Any, Optional, Callable

from authority_resolver import AuthorityResolver
from predictive_engine import simulate_future_u, is_future_stable
from decision_state_recorder import record_decision

# Required existing modules
from u_signal_monitor import compute_u
from stability_governor import evaluate_stability

# Optional hash chain (safe if missing)
try:
    from hash_chain import append_hash
except ImportError:
    append_hash = None


# Initialize authority resolver (in-memory for now)
resolver = AuthorityResolver()


def _normalize_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    return {"raw_result": result}


def execute_proposal(
    proposal: Dict[str, Any],
    previous_receipt_hash: Optional[str] = None,
    receipt_dir: str = "receipts",
) -> Dict[str, Any]:
    """
    Expected proposal format:
    {
        "name": "example_proposal",
        "authority_id": "local_admin",
        "execute": callable,
        ... optional fields for U-signal ...
    }
    """

    # 🔷 0. Authority resolution
    auth_result = resolver.resolve(proposal)

    if not auth_result.get("valid", False):
        return {
            "status": "rejected",
            "stage": "authority",
            "reason": auth_result.get("reason", "authority_resolution_failed"),
            "authority": auth_result,
        }

    # 🔷 1. Predictive stability (future check)
    future_u = simulate_future_u(proposal)

    if not is_future_stable(future_u):
        return {
            "status": "rejected",
            "stage": "predictive",
            "reason": "future_instability",
            "forecast": future_u,
        }

    # 🔷 2. Current U evaluation
    u_value = compute_u(proposal)

    # 🔷 3. Stability decision
    decision = evaluate_stability(u_value)

    if decision.get("action") == "reject":
        return {
            "status": "rejected",
            "stage": "stability",
            "reason": decision.get("reason", "stability_rejection"),
            "u": u_value,
            "decision": decision,
        }

    # 🔷 4. Execute proposal
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

    # 🔷 5. Record decision (receipt)
    receipt = record_decision(
        proposal=proposal,
        result=result,
        u_value=u_value,
        decision=decision,
        authority=auth_result,
        previous_receipt_hash=previous_receipt_hash,
        receipt_dir=receipt_dir,
    )

    # 🔷 6. Append to hash chain (if available)
    if append_hash is not None:
        append_hash(receipt)

    # 🔷 7. Return final result
    return {
        "status": "committed",
        "u": u_value,
        "decision": decision,
        "forecast": future_u,
        "receipt": receipt,
    }
