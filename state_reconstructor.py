import os, json

def reconstruct_state(receipt_dir):
    files = sorted([f for f in os.listdir(receipt_dir) if f.endswith(".json")])
    receipts = []

    for f in files:
        with open(os.path.join(receipt_dir, f)) as fp:
            receipts.append(json.load(fp))

    return {
        "total_executions": len(receipts),
        "authority_drift_detected": len(set(r["authority"]["authority_id"] for r in receipts)) > 1
    }

def print_state_summary(state):
    print("STATE:", state)