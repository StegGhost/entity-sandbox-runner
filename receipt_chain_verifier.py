def verify_chain(receipt_dir):
    if not os.path.exists(receipt_dir):
        return {"status": "ok", "reason": "no receipts"}

    files = sorted(os.listdir(receipt_dir))

    if not files:
        return {"status": "ok", "reason": "empty chain"}

    previous_hash = None

    for idx, fname in enumerate(files):
        path = os.path.join(receipt_dir, fname)

        with open(path, "r") as f:
            receipt = json.load(f)

        # 🔴 verify receipt integrity
        computed_hash = compute_receipt_hash(receipt)
        if computed_hash != receipt.get("receipt_hash"):
            return {
                "status": "rejected",
                "stage": "receipt_integrity",
                "reason": f"tampered receipt at index {idx}"
            }

        # 🔴 FIX: correct first block logic
        if idx == 0:
            if receipt.get("previous_receipt_hash") is not None:
                return {
                    "status": "rejected",
                    "stage": "chain_integrity",
                    "reason": "genesis receipt must have no previous hash"
                }
        else:
            if receipt.get("previous_receipt_hash") != previous_hash:
                return {
                    "status": "rejected",
                    "stage": "chain_integrity",
                    "reason": f"chain break at index {idx}"
                }

        previous_hash = receipt.get("receipt_hash")

    return {"status": "ok"}
