import os
import shutil
import json

from governed_executor import execute_proposal, resolver
from receipt_chain_verifier import clear_chain_lock

RECEIPT_DIR = "receipts"


def reset():
    shutil.rmtree(RECEIPT_DIR, ignore_errors=True)
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    clear_chain_lock(RECEIPT_DIR)


def proposal(name):
    return {
        "name": name,
        "authority_id": "local_admin",
        "execute": lambda: {"ok": True},
    }


def tamper_first_receipt():
    files = [f for f in os.listdir(RECEIPT_DIR) if f.endswith(".json")]
    if not files:
        raise RuntimeError("No receipts to tamper")

    path = os.path.join(RECEIPT_DIR, files[0])

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["result"] = {"tampered": True}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def main():
    reset()

    resolver.register_authority("local_admin", "admin")

    execute_proposal(proposal("test1"), receipt_dir=RECEIPT_DIR)
    execute_proposal(proposal("test2"), receipt_dir=RECEIPT_DIR)

    tamper_first_receipt()

    result = execute_proposal(proposal("test3"), receipt_dir=RECEIPT_DIR)
    print(result)

    assert result["status"] == "rejected", "Tampering was not detected"

    print("Tamper block test successful.")


if __name__ == "__main__":
    main()
