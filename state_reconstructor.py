import os
import json
from receipt_chain_verifier import verify_chain


def reconstruct_state(receipt_dir, strict=False):
    files = sorted(os.listdir(receipt_dir))
    receipts = []

    for f in files:
        path = os.path.join(receipt_dir, f)

        try:
            with open(path, "r") as fp:
                data = json.load(fp)
            receipts.append(data)
        except Exception:
            if strict:
                raise
            continue

    chain_result = verify_chain(receipts)

    if not chain_result["valid"]:
        if strict:
            raise RuntimeError(chain_result["reason"])
        else:
            valid = []
            for i, r in enumerate(receipts):
                if i == 0:
                    valid.append(r)
                    continue

                if r.get("previous_receipt_hash") == valid[-1].get("receipt_hash"):
                    valid.append(r)
                else:
                    break

            receipts = valid

    state = {}
    for r in receipts:
        state[r["proposal"]] = r["result"]

    return state
