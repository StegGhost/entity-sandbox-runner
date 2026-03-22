"""Execution-time admission engine for governed agent actions."""

from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict, List, Tuple


DEFAULT_POLICY_PATH = os.path.join("config", "authority_policy.json")


class AdmissionPolicyError(ValueError):
    """Raised when the authority policy cannot support a requested action."""


SAFE_KEYWORDS = ("read", "list", "query", "status", "inspect")
MODERATE_KEYWORDS = ("send", "write", "update", "schedule", "create")
DANGEROUS_KEYWORDS = ("delete", "remove", "purge", "drop", "revoke")


def load_policy(path: str = DEFAULT_POLICY_PATH) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def classify_action(action: str) -> str:
    value = action.strip().lower()
    if any(keyword in value for keyword in DANGEROUS_KEYWORDS):
        return "dangerous"
    if any(keyword in value for keyword in MODERATE_KEYWORDS):
        return "moderate"
    if any(keyword in value for keyword in SAFE_KEYWORDS):
        return "safe"
    return "unknown"


def hash_state_snapshot(system_state: Dict[str, Any]) -> str:
    canonical = json.dumps(system_state, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def required_capability_for_action(action: str, policy: Dict[str, Any]) -> str:
    action_map = policy.get("action_map", {})
    capability = action_map.get(action)
    if not capability:
        raise AdmissionPolicyError("no_policy_mapping")
    return str(capability)


def is_allowed(capabilities: List[str], action: str, policy: Dict[str, Any]) -> Tuple[bool, str, str | None]:
    try:
        required_capability = required_capability_for_action(action, policy)
    except AdmissionPolicyError as exc:
        return False, str(exc), None

    if required_capability not in capabilities:
        return False, "missing_capability", required_capability

    return True, "allowed", required_capability


def admit_action(passport: Dict[str, Any], action: str, system_state: Dict[str, Any], policy_path: str = DEFAULT_POLICY_PATH) -> Dict[str, Any]:
    policy = load_policy(policy_path)
    capabilities = [str(item) for item in passport.get("capabilities", [])]
    state_hash = hash_state_snapshot(system_state)
    classification = classify_action(action)
    allowed, reason, required_capability = is_allowed(capabilities, action, policy)

    return {
        "timestamp": time.time(),
        "action": action,
        "classification": classification,
        "allowed": allowed,
        "reason": reason,
        "required_capability": required_capability,
        "state_hash": state_hash,
        "policy_version": policy.get("policy_version", "1.0.0"),
    }
