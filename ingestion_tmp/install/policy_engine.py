import json
import os

POLICY_PATH = "config/policy.json"

DEFAULT_POLICY = {
    "hard_stop_u": 0.4,
    "hard_min_u": 0.6,
    "soft_min_u": 0.65
}

def load_policy():
    if not os.path.exists(POLICY_PATH) or os.path.getsize(POLICY_PATH) == 0:
        return DEFAULT_POLICY.copy()
    try:
        with open(POLICY_PATH, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return DEFAULT_POLICY.copy()
        out = DEFAULT_POLICY.copy()
        out.update({k: v for k, v in data.items() if isinstance(v, (int, float))})
        return out
    except Exception:
        return DEFAULT_POLICY.copy()
