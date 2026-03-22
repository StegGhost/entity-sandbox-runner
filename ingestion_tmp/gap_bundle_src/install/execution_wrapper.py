"""Single governed entry point for agent action execution."""

from __future__ import annotations

from typing import Any, Callable, Dict

from governed_passport import assert_valid_passport, hash_passport
from admission_engine import admit_action
from receipt_chain import append_receipt


ExecutorFn = Callable[[str], Dict[str, Any]]


def execute_action(passport: Dict[str, Any], action: str, system_state: Dict[str, Any], executor_fn: ExecutorFn) -> Dict[str, Any]:
    """Admit, execute, and receipt-chain a proposed action.

    Args:
        passport: Agent passport document.
        action: Canonical action key, e.g. "SEND_EMAIL".
        system_state: Snapshot of relevant current system state.
        executor_fn: Callable that performs the action and returns a serializable result.
    """
    assert_valid_passport(passport)
    passport_hash = hash_passport(passport)
    admission = admit_action(passport, action, system_state)

    if not admission["allowed"]:
        return {
            "status": "rejected",
            "reason": admission["reason"],
            "admission": admission,
        }

    execution_result = executor_fn(action)
    receipt = append_receipt(
        passport_hash=passport_hash,
        admission_result=admission,
        execution_result=execution_result,
    )

    return {
        "status": "executed",
        "result": execution_result,
        "receipt": receipt,
    }
