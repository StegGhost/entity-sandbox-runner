import json

REQUIRED_KEYS = {
    "hard_stop_u": 0.3,
    "restrict_u": 0.6,
    "allow_u": 0.85
}

def normalize_policy(policy):
    if not isinstance(policy, dict):
        return REQUIRED_KEYS.copy()

    normalized = REQUIRED_KEYS.copy()
    normalized.update({
        k: v for k, v in policy.items()
        if isinstance(v, (int, float))
    })

    return normalized

def load_policy():
    try:
        with open("config/policy.json") as f:
            return normalize_policy(json.load(f))
    except:
        return REQUIRED_KEYS.copy()
