import os
import json

from receipt_chain_verifier import verify_chain


def reconstruct_state(receipt_dir, strict=True):
    # 🔴 FIX: verify using directory, not list
    chain_result = verify_chain(receipt_dir)

    if strict and chain_result["status"] != "ok":
        raise Exception(f"Chain verification failed: {chain_result}")

    if not os.path.exists(receipt_dir):
        return {}

    files = sorted(os.listdir(receipt_dir))

    state = {}

    for fname in files:
        path = os.path.join(receipt_dir, fname)

        with open(path, "r") as f:
            receipt = json.load(f)

        # apply state transition
        result = receipt.get("result", {})
        if isinstance(result, dict):
            state.update(result)

    return state
