import os
import shutil
import json

from governed_executor import execute_proposal, resolver
from receipt_chain_verifier import clear_chain_lock

RECEIPT_DIR = "receipts"


def reset():
    shutil.rmtree(RECEIPT_DIR, ignore_errors=True)
    os.makedirs(RECEIPT_DIR, exist_ok=True)

    # ✅ FIX: pass directory
    clear_chain_lock(RECEIPT_DIR)


def proposal(name):
    return {
        "name": name,
        "authority_id": "local_admin",
        "execute": lambda: {"ok": True}
    }


def tamper_first_receipt():
    files = sorted(os.listdir(RECEIPT_DIR))
    if not files:
        raise RuntimeError("No receipts to tamper")

    path = os.path.join(RECEIPT_DIR, files[0])

    with open(path, "r") as f:
        data = json.load(f)

    # 🔥 break hash integrity
    data["result"] = {"tampered": True}

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    reset()

    resolver.register_authority("local_admin", "admin")

    # create valid chain
    execute_proposal(proposal("test1"), receipt_dir=RECEIPT_DIR)
    execute_proposal(proposal("test2"), receipt_dir=RECEIPT_DIR)

    # tamper
    tamper_first_receipt()

    # this should now fail on next execution
    result = execute_proposal(proposal("test3"), receipt_dir=RECEIPT_DIR)

    print(result)

    assert result["status"] == "rejected", "Tampering was not detected"

    print("Tamper block test successful.")


if __name__ == "__main__":
    main()
