import os
import json


def verify_chain(input_data):
    if isinstance(input_data, str):
        if not os.path.exists(input_data):
            return {"valid": False, "reason": "receipt_dir_not_found"}

        files = sorted(os.listdir(input_data))
        receipts = []

        for f in files:
            path = os.path.join(input_data, f)
            with open(path, "r") as fp:
                receipts.append(json.load(fp))

    elif isinstance(input_data, list):
        receipts = input_data
    else:
        return {"valid": False, "reason": "invalid_input_type"}

    for i in range(1, len(receipts)):
        prev = receipts[i - 1]
        curr = receipts[i]

        if curr.get("previous_receipt_hash") != prev.get("receipt_hash"):
            return {
                "valid": False,
                "reason": f"chain break at index {i}"
            }

    return {"valid": True}


def is_chain_locked(receipt_dir):
    return os.path.exists(receipt_dir) and len(os.listdir(receipt_dir)) > 0


def clear_chain_lock(receipt_dir):
    return True
