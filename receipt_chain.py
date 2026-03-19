import os
import json


RECEIPT_DIR = "receipts"


def _get_receipt_files(receipt_dir=RECEIPT_DIR):
    if not os.path.isdir(receipt_dir):
        return []

    return sorted([
        f for f in os.listdir(receipt_dir)
        if f.endswith(".json")
    ])


def get_latest_receipt_hash(receipt_dir=RECEIPT_DIR):
    files = _get_receipt_files(receipt_dir)

    if not files:
        return None

    latest_file = files[-1]
    path = os.path.join(receipt_dir, latest_file)

    with open(path, "r", encoding="utf-8") as f:
        receipt = json.load(f)

    return receipt.get("receipt_hash")
