import os
import json
import shutil

from governed_executor import execute_proposal, resolver


RECEIPT_DIR = "receipts"


def demo_execute():
    return {
        "message": "hello from governed execution",
        "ok": True,
    }


def make_proposal(name: str):
    return {
        "name": name,
        "authority_id": "local_admin",
        "execute": demo_execute,
        "coherence": 1.0,
        "authority_validity": 1.0,
        "integrity": 1.0,
        "drift": 0.10,
        "resource_strain": 0.10,
        "entropy": 0.10,
    }


def reset_receipts():
    if os.path.isdir(RECEIPT_DIR):
        shutil.rmtree(RECEIPT_DIR)


def tamper_latest_receipt():
    files = sorted(
        f for f in os.listdir(RECEIPT_DIR)
        if f.endswith(".json")
    )
    if not files:
        raise SystemExit("No receipt files found to tamper with")

    latest_path = os.path.join(RECEIPT_DIR, files[-1])

    with open(latest_path, "r", encoding="utf-8") as f:
        receipt = json.load(f)

    # Tamper with a signed field without recomputing the hash
    receipt["u_value"] = 9999

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    return latest_path


def main():
    reset_receipts()

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    first_result = execute_proposal(make_proposal("baseline_proposal"))
    print("FIRST RESULT:", first_result)

    if first_result.get("status") != "committed":
        raise SystemExit(f"Baseline commit failed: {first_result}")

    tampered_path = tamper_latest_receipt()
    print("TAMPERED RECEIPT:", tampered_path)

    second_result = execute_proposal(make_proposal("post_tamper_proposal"))
    print("SECOND RESULT:", second_result)

    if second_result.get("status") != "rejected":
        raise SystemExit(f"Expected rejection after tampering, got: {second_result}")

    if second_result.get("stage") != "chain_integrity":
        raise SystemExit(f"Expected chain_integrity rejection, got: {second_result}")

    print("Tampering correctly blocked execution.")


if __name__ == "__main__":
    main()
