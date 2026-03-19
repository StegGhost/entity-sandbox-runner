import os
import shutil
import json

from governed_executor import execute_proposal, resolver
from multi_node_verifier import verify_multi_node_state


RECEIPT_DIR = "receipts"
NODE_A_DIR = "receipts_node_a"
NODE_B_DIR = "receipts_node_b"


def demo_execute():
    return {"ok": True}


def make_proposal(name):
    return {
        "name": name,
        "authority_id": "local_admin",
        "execute": demo_execute,
        "coherence": 1.0,
        "authority_validity": 1.0,
        "integrity": 1.0,
        "drift": 0.1,
        "resource_strain": 0.1,
        "entropy": 0.1,
    }


def reset_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


def tamper_node(node_dir):
    files = sorted([
        f for f in os.listdir(node_dir)
        if f.endswith(".json")
    ])

    if not files:
        raise SystemExit("No receipts to tamper")

    latest_path = os.path.join(node_dir, files[-1])

    with open(latest_path, "r", encoding="utf-8") as f:
        receipt = json.load(f)

    # 🔴 Tamper without updating hash
    receipt["u_value"] = 9999

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    return latest_path


def main():
    # 🔷 Clean all state
    reset_dir(RECEIPT_DIR)
    reset_dir(NODE_A_DIR)
    reset_dir(NODE_B_DIR)

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    # 🔷 Build canonical chain
    for i in range(3):
        result = execute_proposal(make_proposal(f"adv_test_{i+1}"))

        if result.get("status") != "committed":
            raise SystemExit(f"Execution {i+1} failed: {result}")

    # 🔷 Copy to both nodes
    shutil.copytree(RECEIPT_DIR, NODE_A_DIR)
    shutil.copytree(RECEIPT_DIR, NODE_B_DIR)

    # 🔴 Tamper ONLY node B
    tampered_file = tamper_node(NODE_B_DIR)
    print("TAMPERED NODE B FILE:", tampered_file)

    # 🔷 Verify divergence
    verification = verify_multi_node_state(
        receipt_dir_a=NODE_A_DIR,
        receipt_dir_b=NODE_B_DIR,
    )

    print("ADVERSARIAL VERIFICATION:", verification)

    if verification["match"]:
        raise SystemExit("Adversarial test failed: tampering not detected")

    print("Adversarial node correctly detected divergence.")


if __name__ == "__main__":
    main()
