import json
import hashlib

def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def hash_data(data):
    return hashlib.sha256(canonical_json(data).encode()).hexdigest()

def score_receipt_risk(receipt):
    admission = receipt.get("result", {}).get("admission", {})
    classification = admission.get("classification", "safe")
    action = receipt.get("action", "")

    score = 0
    reasons = []

    if classification == "dangerous":
        score += 70
        reasons.append("dangerous_classification")
    elif classification == "moderate":
        score += 35
        reasons.append("moderate_classification")
    else:
        score += 10
        reasons.append("safe_classification")

    if "DELETE" in action.upper():
        score += 20
        reasons.append("delete_action")
    if "SEND" in action.upper():
        score += 10
        reasons.append("send_action")

    return {
        "risk_score": min(score, 100),
        "reasons": reasons
    }

def analyze_trajectory(receipts):
    if not receipts:
        return {
            "status": "empty",
            "trajectory_hash": hash_data([]),
            "total_receipts": 0,
            "average_risk": 0,
            "max_risk": 0,
            "drift_detected": False,
            "reasons": []
        }

    scored = []
    reasons = []
    drift_detected = False

    consecutive_moderate_or_higher = 0
    cumulative_risk = 0

    for receipt in receipts:
        risk = score_receipt_risk(receipt)
        scored.append({
            "receipt_hash": receipt.get("receipt_hash"),
            "action": receipt.get("action"),
            "risk_score": risk["risk_score"],
            "reasons": risk["reasons"]
        })

        cumulative_risk += risk["risk_score"]
        reasons.extend(risk["reasons"])

        if risk["risk_score"] >= 35:
            consecutive_moderate_or_higher += 1
        else:
            consecutive_moderate_or_higher = 0

        if consecutive_moderate_or_higher >= 3:
            drift_detected = True

    average_risk = round(cumulative_risk / len(receipts), 2)
    max_risk = max(item["risk_score"] for item in scored)

    if average_risk >= 50:
        drift_detected = True
        reasons.append("high_average_risk")

    if max_risk >= 85:
        drift_detected = True
        reasons.append("extreme_single_step_risk")

    trajectory_core = [
        {
            "receipt_hash": item["receipt_hash"],
            "action": item["action"],
            "risk_score": item["risk_score"]
        }
        for item in scored
    ]

    return {
        "status": "analyzed",
        "trajectory_hash": hash_data(trajectory_core),
        "total_receipts": len(receipts),
        "average_risk": average_risk,
        "max_risk": max_risk,
        "drift_detected": drift_detected,
        "reasons": sorted(set(reasons)),
        "scored_receipts": scored
    }
