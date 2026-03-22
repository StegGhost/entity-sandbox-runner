import argparse
import json
from pathlib import Path


def _load_json(path_str, default):
    if not path_str:
        return default
    path = Path(path_str)
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _analyze_receipts(receipts):
    if not receipts:
        return {
            "trajectory_hash": "none",
            "total_receipts": 0,
            "average_risk": 0.0,
            "max_risk": 0,
            "drift_detected": False,
            "reasons": ["no_receipts"]
        }

    scores = []
    reasons = set()
    max_risk = 0
    consecutive_moderate_or_higher = 0
    drift = False

    for receipt in receipts:
        admission = receipt.get("result", {}).get("admission", {})
        classification = admission.get("classification", "safe")
        action = str(receipt.get("action", "")).upper()

        score = 10
        if classification == "moderate":
            score = 35
            reasons.add("moderate_classification")
        elif classification == "dangerous":
            score = 70
            reasons.add("dangerous_classification")
        else:
            reasons.add("safe_classification")

        if "DELETE" in action:
            score += 20
            reasons.add("delete_action")
        if "SEND" in action:
            score += 10
            reasons.add("send_action")

        score = min(score, 100)
        scores.append(score)
        max_risk = max(max_risk, score)

        if score >= 35:
            consecutive_moderate_or_higher += 1
        else:
            consecutive_moderate_or_higher = 0

        if consecutive_moderate_or_higher >= 3:
            drift = True
            reasons.add("sustained_moderate_or_higher_risk")

    average_risk = round(sum(scores) / len(scores), 2)
    if average_risk >= 50:
        drift = True
        reasons.add("high_average_risk")
    if max_risk >= 85:
        drift = True
        reasons.add("extreme_single_step_risk")

    return {
        "trajectory_hash": f"receipts:{len(receipts)}:{average_risk}:{max_risk}",
        "total_receipts": len(receipts),
        "average_risk": average_risk,
        "max_risk": max_risk,
        "drift_detected": drift,
        "reasons": sorted(reasons)
    }


def select_retry_action(ingest_result, trajectory):
    status = ingest_result.get("status", "unknown")
    if status != "failed":
        return {
            "ingest_status": status,
            "selected_action": "none",
            "rationale": "ingestion_succeeded"
        }

    reason = (
        ingest_result.get("reason")
        or ingest_result.get("capabilities", {}).get("reason")
        or "unknown"
    )

    drift = trajectory.get("drift_detected", False)
    avg_risk = trajectory.get("average_risk", 0)
    max_risk = trajectory.get("max_risk", 0)

    if drift or avg_risk >= 70 or max_risk >= 90:
        action = "quarantine_and_stop"
        rationale = "trajectory_risk_too_high_for_retry"
    elif reason in {"capability_violation", "manifest_missing_required_fields"}:
        action = "repair_and_retry"
        rationale = f"repairable_failure:{reason}"
    elif reason in {"archive_hash_mismatch", "signature_invalid"}:
        action = "quarantine_and_stop"
        rationale = f"integrity_failure:{reason}"
    else:
        action = "safe_retry"
        rationale = f"non_structural_retry:{reason}"

    return {
        "ingest_status": status,
        "selected_action": action,
        "failure_reason": reason,
        "rationale": rationale,
        "trajectory": trajectory
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingest", required=True)
    parser.add_argument("--receipts", default="")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    ingest_result = _load_json(args.ingest, {"status": "unknown"})
    receipts = _load_json(args.receipts, [])
    trajectory = _analyze_receipts(receipts)
    decision = select_retry_action(ingest_result, trajectory)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(decision, f, indent=2)

    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
