"""
AUTHORITY POLICY — minimal stable contract implementation

Purpose:
- provide is_authorized for tests/test_authority_policy.py
- avoid dependency on missing engine.key_registry
- keep behavior deterministic and simple
"""

from __future__ import annotations

from typing import Any, Dict


def _extract_role(authority: Any) -> str:
    if isinstance(authority, dict):
        return str(authority.get("role", "")).strip().lower()
    return ""


def _extract_valid(authority: Any) -> bool:
    if isinstance(authority, dict):
        return bool(authority.get("valid", True))
    return False


def is_authorized(authority: Dict[str, Any], action: str | None = None) -> bool:
    """
    Minimal deterministic authorization policy.

    Rules:
    - authority must be a dict
    - authority["valid"] must not be False
    - role "admin" is authorized
    - role "operator" is authorized
    - anything else is denied
    """
    if not isinstance(authority, dict):
        return False

    if not _extract_valid(authority):
        return False

    role = _extract_role(authority)
    if role in {"admin", "operator"}:
        return True

    return False


def evaluate_authority(authority: Dict[str, Any], action: str | None = None) -> Dict[str, Any]:
    """
    Optional helper for downstream callers.
    """
    allowed = is_authorized(authority, action=action)
    return {
        "authorized": allowed,
        "action": action,
        "authority": authority,
    }
