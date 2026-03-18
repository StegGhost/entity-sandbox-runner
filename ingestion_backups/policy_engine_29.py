import json

REQUIRED_KEYS = {
    "hard_stop_u": 0.3,
    "restrict_u": 0.6,
    "allow_u": 0.85,
}


def normalize_policy(policy):
    if not isinstance(policy, dict):
        return REQUIRED_KEYS.copy()

    normalized = REQUIRED_KEYS.copy()
    normalized.update(
        {
            k: v
            for k, v in policy.items()
            if k in REQUIRED_KEYS and isinstance(v, (int, float))
        }
    )
    return normalized


def validate_remote_policy(policy):
    if not isinstance(policy, dict):
        return False

    # Require all three keys to be present and numeric
    for key in REQUIRED_KEYS:
        if key not in policy or not isinstance(policy[key], (int, float)):
            return False

    hard_stop_u = policy["hard_stop_u"]
    restrict_u = policy["restrict_u"]
    allow_u = policy["allow_u"]

    # Enforce sane BCAT ordering
    if not (0.0 <= hard_stop_u < restrict_u < allow_u <= 1.0):
        return False

    return True


def load_policy():
    try:
        with open("config/policy.json", "r") as f:
            return normalize_policy(json.load(f))
    except Exception:
        return REQUIRED_KEYS.copy()
