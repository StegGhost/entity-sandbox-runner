import os
import shutil

from governed_executor import execute_proposal, resolver
from state_reconstructor import reconstruct_state
from receipt_chain_verifier import clear_chain_lock

RECEIPT_DIR = "receipts"


def reset():
    shutil.rmtree(RECEIPT_DIR, ignore_errors=True)
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    clear_chain_lock(RECEIPT_DIR)


def proposal(name, value):
    return {
        "name": name,
        "authority_id": "local_admin",
        "execute": lambda: value,
    }


def main():
    reset()

    resolver.register_authority("local_admin", "admin")

    execute_proposal(proposal("test1", {"a": 1}), receipt_dir=RECEIPT_DIR)
    execute_proposal(proposal("test2", {"b": 2}), receipt_dir=RECEIPT_DIR)
    execute_proposal(proposal("test3", {"c": 3}), receipt_dir=RECEIPT_DIR)

    state = reconstruct_state(RECEIPT_DIR, strict=True)
    print("RECONSTRUCTED STATE:", state)

    assert state == {"a": 1, "b": 2, "c": 3}, "State reconstruction failed"

    print("State reconstruction test successful.")


if __name__ == "__main__":
    main()
