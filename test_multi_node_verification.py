import os
import shutil

from governed_executor import execute_proposal, resolver
from multi_node_verifier import verify_nodes

NODE_A = "receipts_node_a"
NODE_B = "receipts_node_b"


def reset():
    shutil.rmtree(NODE_A, ignore_errors=True)
    shutil.rmtree(NODE_B, ignore_errors=True)
    os.makedirs(NODE_A, exist_ok=True)
    os.makedirs(NODE_B, exist_ok=True)


def proposal(name):
    return {
        "name": name,
        "authority_id": "local_admin",
        "execute": lambda: {"ok": True}
    }


def run_node(node_dir):
    return [
        execute_proposal(proposal("test1"), receipt_dir=node_dir),
        execute_proposal(proposal("test2"), receipt_dir=node_dir),
        execute_proposal(proposal("test3"), receipt_dir=node_dir),
    ]


def main():
    reset()

    resolver.register_authority("local_admin", "admin")

    results_a = run_node(NODE_A)
    results_b = run_node(NODE_B)

    for i, r in enumerate(results_a + results_b, start=1):
        if r["status"] != "committed":
            raise SystemExit(f"Execution {i} failed: {r}")

    verification = verify_nodes([NODE_A, NODE_B])

    print("VERIFICATION:", verification)

    assert verification["consensus"], "Nodes do not agree on state"

    print("Multi-node verification successful.")


if __name__ == "__main__":
    main()
