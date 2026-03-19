def reach_consensus(results):
    approvals = [r for r in results if r["decision"] == "allow"]

    if len(approvals) >= (len(results) // 2 + 1):
        return True

    return False
