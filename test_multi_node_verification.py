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


def copy_receipts(src, dst):
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    reset_dir(RECEIPT_DIR)
    reset_dir(NODE_A_DIR)
    reset_dir(NODE_B_DIR)

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    result_1 = execute_proposal(make_proposal("node_test_1"))
    result_2 = execute_proposal(make_proposal("node_test_2"))
    result_3 = execute_proposal(make_proposal("node_test_3"))

    if result_1.get("status") != "committed":
        raise SystemExit(f"Execution 1 failed: {result_1}")
    if result_2.get("status") != "committed":
        raise SystemExit(f"Execution 2 failed: {result_2}")
    if result_3.get("status") != "committed":
        raise SystemExit(f"Execution 3 failed: {result_3}")

    copy_receipts(RECEIPT_DIR, NODE_A_DIR)
    copy_receipts(RECEIPT_DIR, NODE_B_DIR)

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
