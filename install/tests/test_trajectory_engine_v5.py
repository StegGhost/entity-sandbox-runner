from install.engine.trajectory_engine_v5 import score_receipt_risk, analyze_trajectory

def test_score_receipt_risk_safe():
    receipt = {
        "action": "READ_EMAIL",
        "result": {
            "admission": {
                "classification": "safe"
            }
        }
    }
    result = score_receipt_risk(receipt)
    assert result["risk_score"] >= 10

def test_analyze_trajectory_detects_drift():
    receipts = [
        {
            "receipt_hash": "r1",
            "action": "SEND_EMAIL",
            "result": {"admission": {"classification": "moderate"}}
        },
        {
            "receipt_hash": "r2",
            "action": "SEND_EMAIL",
            "result": {"admission": {"classification": "moderate"}}
        },
        {
            "receipt_hash": "r3",
            "action": "DELETE_FILE",
            "result": {"admission": {"classification": "dangerous"}}
        }
    ]
    result = analyze_trajectory(receipts)
    assert result["drift_detected"] is True
    assert result["total_receipts"] == 3
