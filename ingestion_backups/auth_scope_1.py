import hashlib
import json
import os
from typing import Dict, Any

AUTH_POLICY_PATH = "config/auth_policy.json"

DEFAULT_POLICY = {
    "levels": {
        "chain_maintenance": 0,
        "experiment_metadata": 1,
        "experiment_content": 2,
        "replay_restricted": 3,
        "governance_control": 4
    }
}

def load_auth_policy() -> Dict[str, Any]:
    if not os.path.exists(AUTH_POLICY_PATH) or os.path.getsize(AUTH_POLICY_PATH) == 0:
        return DEFAULT_POLICY
    try:
        with open(AUTH_POLICY_PATH, "r") as f:
            policy = json.load(f)
        if not isinstance(policy, dict):
            return DEFAULT_POLICY
        return policy
    except Exception:
        return DEFAULT_POLICY

def hash_owner_id(owner_id: str) -> str:
    return hashlib.sha256(owner_id.encode()).hexdigest()

def auth_level_for_class(auth_class: str) -> int:
    policy = load_auth_policy()
    return int(policy.get("levels", {}).get(auth_class, 999))

def build_scope_record(owner_id: str, visibility: str, auth_class: str) -> Dict[str, Any]:
    return {
        "owner_id_hash": hash_owner_id(owner_id),
        "visibility": visibility,
        "auth_class": auth_class,
        "required_level": auth_level_for_class(auth_class),
    }
