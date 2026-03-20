import os
import shutil

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


def main():
    reset()

    resolver.register_authority("local_admin", "admin")

    results = [
        execute_proposal(proposal("test1"), receipt_dir=RECEIPT_DIR),
        execute_proposal(proposal("test2"), receipt_dir=RECEIPT_DIR),
        execute_proposal(proposal("test3"), receipt_dir=RECEIPT_DIR),
    ]

    for result in results:
        print(result)
        if result["status"] != "committed":
            raise SystemExit(f"Execution failed: {result}")

    print("Governed executor test successful.")


if __name__ == "__main__":
    main()
