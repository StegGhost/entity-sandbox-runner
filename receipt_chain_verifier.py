import os
import json
import hashlib


def compute_hash(data):
    encoded = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_receipts(receipt_dir):
    receipts = []
    for fname in os.listdir(receipt_dir):
        if fname.endswith(".json"):
            with open(os.path.join(receipt_dir, fname), "r") as f:
                receipts.append(json.load(f))
    return receipts


def build_chain(receipts):
    by_prev = {}
    genesis = None

    for r in receipts:
        prev = r.get("previous_receipt_hash")
        if prev is None:
            genesis = r
        else:
            by_prev[prev] = r

    if not genesis:
        raise Exception("no genesis receipt")

    ordered = [genesis]

    while True:
        current = ordered[-1]
        nxt = by_prev.get(current["receipt_hash"])
        if not nxt:
            break
        ordered.append(nxt)

    return ordered


def verify_chain(receipt_dir):
    if not os.path.exists(receipt_dir):
        return {"status": "ok"}

    receipts = load_receipts(receipt_dir)

    if not receipts:
        return {"status": "ok"}

    try:
        ordered = build_chain(receipts)
    except Exception as e:
        return {"status": "rejected", "reason": str(e)}

    prev_hash = None
    prev_process_hash = None

    for i, r in enumerate(ordered):
        expected_hash = compute_hash({k: v for k, v in r.items() if k != "receipt_hash"})
        if expected_hash != r["receipt_hash"]:
            return {"status": "rejected", "reason": f"tampered receipt {i}"}

        if i == 0:
            if r["previous_receipt_hash"] is not None:
                return {"status": "rejected", "reason": "invalid genesis"}
        else:
            if r["previous_receipt_hash"] != prev_hash:
                return {"status": "rejected", "reason": f"chain break {i}"}

        # 🔥 NEW: process chain validation
        process_material = {
            "previous_process_hash": prev_process_hash,
            "receipt_hash": r["receipt_hash"],
            "execution_fingerprint": r["execution_fingerprint"]
        }

        expected_process = compute_hash(process_material)

        if r.get("process_hash") != expected_process:
            return {
                "status": "rejected",
                "reason": f"process hash mismatch at {i}"
            }

        prev_hash = r["receipt_hash"]
        prev_process_hash = r["process_hash"]

    return {"status": "ok"}
