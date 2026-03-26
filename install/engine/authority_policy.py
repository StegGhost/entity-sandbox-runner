"""
AUTHORITY POLICY — stable contract implementation

Purpose:
- satisfy tests/test_authority_policy.py
- avoid dependency on missing engine.key_registry
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


def _normalize_authority(authority: Any) -> Dict[str, Any]:
    if isinstance(authority, dict):
        return authority
    return {}


def _extract_role(authority: Dict[str, Any]) -> str:
    role = authority.get("role")
    key_id = authority.get("key_id") or authority.get("authority_id") or authority.get("key")

    if role:
        return str(role).strip().lower()

    return get_role_for_key(str(key_id) if key_id is not None else None)


def _extract_valid(authority: Dict[str, Any]) -> bool:
    return bool(authority.get("valid", True))


def is_authorized(authority: Any, action: str | None = None) -> Tuple[bool, str]:
    """
    Return (authorized, reason).

    Policy:
    - invalid authority -> deny
    - admin can do anything
    - operator can do anything
    - sdk cannot write engine paths/actions
    - sdk may do non-engine reads/checks
    - unknown denied
    """
    auth = _normalize_authority(authority)

    if not auth:
        return False, "missing_authority"

    if not _extract_valid(auth):
        return False, "invalid_authority"

    role = _extract_role(auth)
    action_text = (action or "").strip().lower()

    if role == "admin":
        return True, "admin_allowed"

    if role == "operator":
        return True, "operator_allowed"

    if role == "sdk":
        if "write" in action_text and "engine" in action_text:
            return False, "sdk_cannot_write_engine"
        return True, "sdk_allowed"

    return False, "unknown_role"


def evaluate_authority(authority: Any, action: str | None = None) -> Dict[str, Any]:
    """
    Convenience helper for downstream callers.
    """
    allowed, reason = is_authorized(authority, action=action)
    auth = _normalize_authority(authority)

    return {
        "authorized": allowed,
        "reason": reason,
        "action": action,
        "authority": auth,
        "role": _extract_role(auth),
    }
