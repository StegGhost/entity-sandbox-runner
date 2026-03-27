def reconcile_execution_state(execution_result):
    """
    Now receipt-aware reconciliation
    """

    if execution_result.get("status") != "ok":
        return {
            "status": "needs_retry",
            "reason": execution_result.get("error")
        }

    receipt = execution_result.get("execution", {}).get("receipt")

    if not receipt:
        return {
            "status": "invalid",
            "reason": "missing_receipt"
        }

    if not receipt.get("policy_passed"):
        return {
            "status": "rejected",
            "reason": "policy_failed"
        }

    return {
        "status": "committed",
        "receipt_id": receipt.get("receipt_id")
    }
