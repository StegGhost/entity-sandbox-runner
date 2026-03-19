import os
import json

from governed_executor import execute_proposal
from receipt_chain_verifier import clear_chain_lock

RECEIPT_DIR = "receipts"


def sample_proposal():
    return {
        "proposal": "baseline_proposal",
        "execute": lambda: {
            "message": "hello from governed execution",
            "ok": True
        }
    }


def tamper_receipt():
    if not os.path.exists(RECEIPT_DIR):
        raise Exception("Receipts directory does not exist")

    files = sorted([
        f for f in os.listdir(RECEIPT_DIR)
        if f.endswith(".json")
    ])

    if not files:
        raise Exception("No receipts found to tamper")

    path = os.path.join(RECEIPT_DIR, files[0])

    with open(path, "r") as f:
        data = json.load(f)

    # 🔴 Tamper WITHOUT recomputing hash
    data["tampered"] = True

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"TAMPERED RECEIPT: {path}")


def main():
    clear_chain_lock()

    # Clean start
    os.system("rm -rf receipts && mkdir receipts")

    # ✅ STEP 1 — create receipt
    first = execute_proposal(sample_proposal())
    print("FIRST RESULT:", first)

    assert first["status"] == "committed", "Initial execution failed"

    # ✅ Ensure receipt exists
    files = os.listdir(RECEIPT_DIR)
    assert len(files) > 0, "No receipt created"

    # ✅ STEP 2 — tamper
    tamper_receipt()

    # ✅ STEP 3 — attempt execution (must fail)
    second = execute_proposal({
        "proposal": "post_tamper_proposal",
        "execute": lambda: {"message": "should not execute"}
    })

    print("SECOND RESULT:", second)

    assert second["status"] == "rejected"
    assert second["stage"] in ["chain_integrity", "chain_locked"]

    print("Tampering correctly blocked execution.")


if __name__ == "__main__":
    main()
