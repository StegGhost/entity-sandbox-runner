import os
import shutil

from governed_executor import execute_proposal, resolver
from state_reconstructor import reconstruct_state


RECEIPT_DIR = "receipts"


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


def reset_environment():
    if os.path.isdir(RECEIPT_DIR):
        shutil.rmtree(RECEIPT_DIR)


def main():
    # 🔷 HARD RESET (THIS IS THE FIX)
    reset_environment()

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    # 🔷 Build fresh clean chain
    for i in range(3):
        result = execute_proposal(make_proposal(f"reconstruct_test_{i+1}"))

        if result.get("status") != "committed":
            raise SystemExit(f"Execution {i+1} failed: {result}")

    # 🔷 Now reconstruct
    state = reconstruct_state(RECEIPT_DIR)

    print("\n=== RECONSTRUCTED SYSTEM STATE ===")
    print(f"Total Executions: {state['total_executions']}")
    print(f"Last U: {state['last_u']}")
    print(f"Last Decision: {state['last_decision']}")
    print(f"Authorities: {state['authorities']}")
    print("=================================\n")

    print("State reconstruction successful.")


if __name__ == "__main__":
    main()
