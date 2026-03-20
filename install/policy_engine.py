import json
import os
from typing import Dict

POLICY_PATH = "config/policy.json"

DEFAULT_POLICY = {
    # --- U-signal thresholds ---
    "hard_stop_u": 0.4,   # below this → reject immediately
    "hard_min_u": 0.6,    # below this → reject unless override
    "soft_min_u": 0.65,   # below this → allow but caution

    # --- execution controls ---
    "require_consensus_high_risk": True,
    "min_trust_score": 0.5,

    # --- risk classification ---
    "high_risk_actions": ["delete", "transfer", "shutdown"],
    "medium_risk_actions": ["update", "modify"]
}


# -------------------------------
# Load policy
# -------------------------------
def load_policy() -> Dict:
    if not os.path.exists(POLICY_PATH) or os.path.getsize(POLICY_PATH) == 0:
        return DEFAULT_POLICY.copy()

    try:
        with open(POLICY_PATH, "r") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return DEFAULT_POLICY.copy()

        out = DEFAULT_POLICY.copy()

        # only allow valid numeric / list overrides
        for k, v in data.items():
            if isinstance(v, (int, float, list, bool)):
                out[k] = v

        return out

    except Exception:
        return DEFAULT_POLICY.copy()


# -------------------------------
# Risk classification
# -------------------------------
def classify_risk(proposal: dict, policy: Dict) -> str:
    name = proposal.get("name", "")

    if any(k in name for k in policy["high_risk_actions"]):
        return "high"

    if any(k in name for k in policy["medium_risk_actions"]):
        return "medium"

    return "low"


# -------------------------------
# U-signal enforcement
# -------------------------------
def evaluate_u_signal(u: float, policy: Dict) -> dict:
    if u < policy["hard_stop_u"]:
        return {"allowed": False, "reason": "u_hard_stop"}

    if u < policy["hard_min_u"]:
        return {"allowed": False, "reason": "u_below_hard_min"}

    if u < policy["soft_min_u"]:
        return {"allowed": True, "warning": "u_soft_zone"}

    return {"allowed": True}


# -------------------------------
# Full policy evaluation
# -------------------------------
def evaluate_policy(proposal: dict, u_signal: float, model_score: float) -> dict:
    policy = load_policy()

    # ---- U-signal gate ----
    u_result = evaluate_u_signal(u_signal, policy)
    if not u_result["allowed"]:
        return u_result

    # ---- Trust gate ----
    if model_score < policy["min_trust_score"]:
        return {"allowed": False, "reason": "low_model_trust"}

    # ---- Risk classification ----
    risk = classify_risk(proposal, policy)

    return {
        "allowed": True,
        "risk": risk,
        "require_consensus": (
            risk == "high" and policy["require_consensus_high_risk"]
        ),
        "warning": u_result.get("warning")
    }
