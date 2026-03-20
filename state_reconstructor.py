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

        except Exception as e:
            if strict:
                raise
            else:
                continue

    # 🔥 attempt chain verification
    chain_result = verify_chain(receipts)

    if not chain_result["valid"]:
        if strict:
            raise RuntimeError(chain_result["reason"])
        else:
            # 🔥 filter valid prefix only
            valid_receipts = []
            for i, r in enumerate(receipts):
                if i == 0:
                    valid_receipts.append(r)
                    continue

                if r.get("previous_receipt_hash") == valid_receipts[-1].get("receipt_hash"):
                    valid_receipts.append(r)
                else:
                    break

            receipts = valid_receipts

    # 🔥 build final state
    state = {}

    for r in receipts:
        state[r["proposal"]] = r["result"]

    return state
