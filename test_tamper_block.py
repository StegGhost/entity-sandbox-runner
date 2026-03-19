import os
import json

from governed_executor import execute_proposal
from receipt_chain_verifier import clear_chain_lock

RECEIPT_DIR = "receipts"


def sample_proposal():
    return {
        "proposal": "baseline_proposal",
        "execute": lambda: {"message": "hello from governed execution", "ok": True}
    }


def tamper_receipt():
    files = sorted(os.listdir(RECEIPT_DIR))
    path = os.path.join(RECEIPT_DIR, files[0])

    with open(path, "r") as f:
        data = json.load(f)

    data["tampered"] = True

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"TAMPERED RECEIPT: {path}")


def main():
    clear_chain_lock()

    os.system("rm -rf receipts && mkdir receipts")

    # First valid execution
    execute_proposal(sample_proposal())

    # Tamper
    tamper_receipt()

    # Second execution SHOULD FAIL
    result = execute_proposal({
        "proposal": "post_tamper_proposal",
        "execute": lambda: {"message": "should not execute"}
    })

    print("SECOND RESULT:", result)

    assert result["status"] == "rejected"
    assert result["stage"] in ["chain_integrity", "chain_locked"]

    print("Tampering correctly blocked execution.")


if __name__ == "__main__":
    main()
