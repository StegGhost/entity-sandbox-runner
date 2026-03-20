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
        "execute": lambda: {"ok": True},
    }


def run_node(node_dir):
    return [
        execute_proposal(proposal("test1"), receipt_dir=node_dir),
        execute_proposal(proposal("test2"), receipt_dir=node_dir),
        execute_proposal(proposal("test3"), receipt_dir=node_dir),
    ]


def tamper(node_dir):
    files = [f for f in os.listdir(node_dir) if f.endswith(".json")]
    if not files:
        raise RuntimeError("No receipts to tamper")

    path = os.path.join(node_dir, files[0])

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["result"] = {"tampered": True, "ok": True}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def main():
    reset()

    resolver.register_authority("local_admin", "admin")

    results_a = run_node(NODE_A)
    results_b = run_node(NODE_B)

    for result in results_a + results_b:
        if result["status"] != "committed":
            raise SystemExit(f"Execution failed: {result}")

    tamper(NODE_B)

    verification = verify_nodes([NODE_A, NODE_B])
    print("VERIFICATION:", verification)

    assert not verification["consensus"], "Tampered node was not detected"

    print("Adversarial node detection successful.")


if __name__ == "__main__":
    main()
