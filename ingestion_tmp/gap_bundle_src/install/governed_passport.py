"""Governed Agent Passport utilities.

This module provides lightweight helpers for validating, normalizing,
and hashing AI agent passport documents. It is designed to be ingestion-
friendly, dependency-light, and easy to embed into an execution-governance
pipeline.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Tuple


REQUIRED_TOP_LEVEL_FIELDS = (
    "standard",
    "version",
    "agent",
    "capabilities",
    "public_key",
    "signature",
)


class PassportValidationError(ValueError):
    """Raised when a passport fails structural validation."""


def canonicalize_passport(passport: Dict[str, Any]) -> str:
    """Return a deterministic JSON string for hashing and comparison.

    This uses sorted keys and compact separators for portability.
    """
    return json.dumps(passport, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hash_passport(passport: Dict[str, Any]) -> str:
    """Return a SHA-256 hash of the canonicalized passport document."""
    canonical = canonicalize_passport(passport).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def extract_capabilities(passport: Dict[str, Any]) -> List[str]:
    """Return the passport capability list as strings."""
    capabilities = passport.get("capabilities", [])
    if not isinstance(capabilities, list):
        raise PassportValidationError("capabilities must be a list")
    return [str(item) for item in capabilities]


def get_agent_id(passport: Dict[str, Any]) -> str:
    """Return the agent ID from the passport."""
    agent = passport.get("agent", {})
    if not isinstance(agent, dict):
        raise PassportValidationError("agent must be an object")
    agent_id = agent.get("id")
    if not agent_id:
        raise PassportValidationError("agent.id is required")
    return str(agent_id)


def validate_passport_structure(passport: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate the required shape of a passport.

    Returns:
        (True, "valid") on success, otherwise (False, reason).
    """
    if not isinstance(passport, dict):
        return False, "passport_not_object"

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in passport:
            return False, f"missing_{field}"

    agent = passport.get("agent")
    if not isinstance(agent, dict):
        return False, "agent_not_object"

    if "id" not in agent:
        return False, "missing_agent_id"

    if "name" not in agent:
        return False, "missing_agent_name"

    capabilities = passport.get("capabilities")
    if not isinstance(capabilities, list):
        return False, "capabilities_not_list"

    return True, "valid"


def assert_valid_passport(passport: Dict[str, Any]) -> None:
    """Raise an exception if the passport is invalid."""
    ok, reason = validate_passport_structure(passport)
    if not ok:
        raise PassportValidationError(reason)
