import os
import shutil

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


def main():
    # 🔷 HARD RESET ALL STATE
    reset_dir(RECEIPT_DIR)
    reset_dir(NODE_A_DIR)
    reset_dir(NODE_B_DIR)

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    # 🔷 Build clean canonical chain
    for i in range(3):
        result = execute_proposal(make_proposal(f"node_test_{i+1}"))

        if result.get("status") != "committed":
            raise SystemExit(f"Execution {i+1} failed: {result}")

    # 🔷 Copy clean state to two nodes
    shutil.copytree(RECEIPT_DIR, NODE_A_DIR)
    shutil.copytree(RECEIPT_DIR, NODE_B_DIR)

    # 🔷 Verify independent reconstruction
    verification = verify_multi_node_state(
        receipt_dir_a=NODE_A_DIR,
        receipt_dir_b=NODE_B_DIR,
    )

    print("MULTI-NODE VERIFICATION:", verification)

    if not verification["match"]:
        raise SystemExit(
            f"Multi-node verification failed: "
            f"{verification['hash_a']} != {verification['hash_b']}"
        )

    print("Multi-node verification successful.")


if __name__ == "__main__":
    main()
