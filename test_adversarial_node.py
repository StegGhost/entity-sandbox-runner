import os
import shutil
import json

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


def tamper(node_dir):
    files = sorted(os.listdir(node_dir))
    if not files:
        raise RuntimeError("No receipts to tamper with")

    path = os.path.join(node_dir, files[0])

    with open(path, "r") as f:
        data = json.load(f)

    # 🔥 corrupt the receipt
    data["result"] = {"tampered": True}

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    reset()

    resolver.register_authority("local_admin", "admin")

    # run both nodes
    results_a = run_node(NODE_A)
    results_b = run_node(NODE_B)

    for r in results_a + results_b:
        if r["status"] != "committed":
            raise SystemExit(f"Execution failed: {r}")

    # 🔥 introduce adversarial tampering
    tamper(NODE_B)

    verification = verify_nodes([NODE_A, NODE_B])

    print("VERIFICATION:", verification)

    assert not verification["consensus"], "Tampered node was not detected"

    print("Adversarial node detection successful.")


if __name__ == "__main__":
    main()
