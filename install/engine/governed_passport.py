"""
GOVERNED PASSPORT — minimal stable contract implementation

Purpose:
- provide deterministic passport hashing
- satisfy execution_pipeline_v4 imports
- keep behavior simple and explicit while the sandbox baseline is stabilized
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def _canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)


def hash_passport(passport: Dict[str, Any]) -> str:
    """
    Deterministically hash a passport payload.
    """
    payload = _canonical_json(passport).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_passport(
    identity: Dict[str, Any],
    authority: Dict[str, Any],
    constraints: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Construct a normalized governed passport object.
    """
    passport = {
        "identity": identity or {},
        "authority": authority or {},
        "constraints": constraints or {},
    }
    passport["passport_hash"] = hash_passport(passport)
    return passport


def verify_passport(passport: Dict[str, Any]) -> bool:
    """
    Verify that a passport carries a valid deterministic hash.
    """
    if not isinstance(passport, dict):
        return False

    existing = passport.get("passport_hash")
    if not existing:
        return False

    clone = dict(passport)
    clone.pop("passport_hash", None)
    expected = hash_passport(clone)
    return existing == expected


def passport_summary(passport: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a compact summary that downstream code can safely inspect.
    """
    return {
        "identity": passport.get("identity", {}),
        "authority": passport.get("authority", {}),
        "constraints": passport.get("constraints", {}),
        "passport_hash": passport.get("passport_hash"),
        "valid": verify_passport(passport),
    }
