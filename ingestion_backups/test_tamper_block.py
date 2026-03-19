import os
import json
import shutil

from governed_executor import execute_proposal, resolver
from receipt_chain_verifier import clear_chain_lock

RECEIPT_DIR = "receipts"


def reset_environment():
    clear_chain_lock()

    if os.path.isdir(RECEIPT_DIR):
        shutil.rmtree(RECEIPT_DIR)

    os.makedirs(RECEIPT_DIR, exist_ok=True)


def sample_proposal(name: str):
    return {
        "name": name,
        "authority_id": "local_admin",
        "execute": lambda: {
            "message": "hello from governed execution",
            "ok": True,
        },
        "coherence": 1.0,
        "authority_validity": 1.0,
        "integrity": 1.0,
        "drift": 0.10,
        "resource_strain": 0.10,
        "entropy": 0.10,
    }


def tamper_receipt():
    if not os.path.exists(RECEIPT_DIR):
        raise Exception("Receipts directory does not exist")

    files = sorted(
        f for f in os.listdir(RECEIPT_DIR)
        if f.endswith(".json")
    )

    if not files:
        raise Exception("No receipts found to tamper")

    path = os.path.join(RECEIPT_DIR, files[0])

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Tamper without recomputing the receipt hash
    data["u_value"] = 9999

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)

    print(f"TAMPERED RECEIPT: {path}")


def main():
    reset_environment()

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    first = execute_proposal(sample_proposal("baseline_proposal"))
    print("FIRST RESULT:", first)

    assert first["status"] == "committed", "Initial execution failed"

    files = [f for f in os.listdir(RECEIPT_DIR) if f.endswith(".json")]
    assert len(files) > 0, "No receipt created"

    tamper_receipt()

    second = execute_proposal(sample_proposal("post_tamper_proposal"))
    print("SECOND RESULT:", second)

    assert second["status"] == "rejected", "Tampering was not blocked"
    assert second["stage"] in ["chain_integrity", "chain_locked"], "Wrong rejection stage"

    print("Tampering correctly blocked execution.")


if __name__ == "__main__":
    main()
