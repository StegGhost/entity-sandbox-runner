import os
import json
import hashlib

RECEIPT_DIR = "receipts"


def _hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def _ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_latest_receipt_hash(receipt_dir=RECEIPT_DIR):
    if not os.path.exists(receipt_dir):
        return None

    files = sorted(os.listdir(receipt_dir))
    if not files:
        return None

    last = files[-1]
    with open(os.path.join(receipt_dir, last), "r") as f:
        receipt = json.load(f)

    return receipt.get("receipt_hash")


def append_receipt(receipt: dict, receipt_dir=RECEIPT_DIR):
    _ensure_dir(receipt_dir)

    serialized = json.dumps(receipt, sort_keys=True)
    receipt_hash = _hash(serialized)

    receipt["receipt_hash"] = receipt_hash

    index = len(os.listdir(receipt_dir))
    path = os.path.join(receipt_dir, f"{index:06d}.json")

    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    return receipt
