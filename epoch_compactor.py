import os
import json
import hashlib
from typing import List


def _hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def _load_receipts(receipt_dir: str) -> List[dict]:
    files = sorted(
        [f for f in os.listdir(receipt_dir) if f.endswith(".json")]
    )
    receipts = []
    for f in files:
        with open(os.path.join(receipt_dir, f), "r") as fh:
            receipts.append(json.load(fh))
    return receipts


def _merkle_root(hashes: List[str]) -> str:
    if not hashes:
        return _hash("empty")

    level = hashes[:]
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            next_level.append(_hash(left + right))
        level = next_level
    return level[0]


def compact_epoch(receipt_dir: str, epoch_size: int = 10):
    receipts = _load_receipts(receipt_dir)

    if len(receipts) < epoch_size:
        return {"status": "skipped", "reason": "not enough receipts"}

    epoch = receipts[:epoch_size]

    hashes = [r["receipt_hash"] for r in epoch]
    root = _merkle_root(hashes)

    epoch_record = {
        "epoch_size": epoch_size,
        "root_hash": root,
        "receipts_included": len(epoch),
    }

    with open(os.path.join(receipt_dir, f"epoch_{root}.json"), "w") as f:
        json.dump(epoch_record, f, indent=2)

    return {
        "status": "compacted",
        "root_hash": root,
        "count": len(epoch),
    }
