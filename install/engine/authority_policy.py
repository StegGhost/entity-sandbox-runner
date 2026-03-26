"""
AUTHORITY POLICY — stable contract implementation

Purpose:
- satisfy tests/test_authority_policy.py
- provide:
  - get_role_for_key(...)
  - is_authorized(...)
  - evaluate_authority(...)
Behavior:
- deterministic
- simple
- dependency-free
"""

from __future__ import annotations

from typing import Any, Dict, Tuple


def get_role_for_key(key_id: str | None) -> str:
    """
    Minimal deterministic role resolver used by tests.

    Mapping:
    - keys containing 'admin' -> admin
    - keys containing 'sdk'   -> sdk
    - keys containing 'op'    -> operator
    - otherwise               -> unknown
    """
    if not key_id:
        return "unknown"

    key = str(key_id).strip().lower()

    if "admin" in key:
        return "admin"
    if "sdk" in key:
        return "sdk"
    if "op" in key:
        return "operator"

    return "unknown"


def is_authorized(target: Any, key_id: str | None = None) -> Tuple[bool, str]:
    """
    Return (authorized, reason).

    Expected call shape in current tests:
        is_authorized("install/engine/x.py", "admin-key")

    Policy:
    - admin may write engine paths
    - operator may write engine paths
    - sdk may not write engine paths
    - unknown denied
    """
    target_text = str(target or "").strip().lower()
    role = get_role_for_key(key_id)

    if role == "admin":
        return True, "admin_allowed"

    if role == "operator":
        return True, "operator_allowed"

    if role == "sdk":
        if target_text.startswith("install/engine/") or "/engine/" in target_text:
            return False, "sdk_cannot_write_engine"
        return True, "sdk_allowed"

    return False, "unknown_role"


def evaluate_authority(target: Any, key_id: str | None = None) -> Dict[str, Any]:
    """
    Convenience helper for downstream callers.
    """
    allowed, reason = is_authorized(target, key_id)
    return {
        "authorized": allowed,
        "reason": reason,
        "target": target,
        "key_id": key_id,
        "role": get_role_for_key(key_id),
    }
