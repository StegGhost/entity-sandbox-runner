import os
import shutil

from governed_executor import execute_proposal, resolver
from state_reconstructor import reconstruct_state, print_state_summary
from state_hash import compute_state_hash


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


def reset():
    if os.path.isdir(RECEIPT_DIR):
        shutil.rmtree(RECEIPT_DIR)


def main():
    reset()

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    result_1 = execute_proposal(make_proposal("step_1"))
    result_2 = execute_proposal(make_proposal("step_2"))
    result_3 = execute_proposal(make_proposal("step_3"))

    if result_1.get("status") != "committed":
        raise SystemExit(f"Execution 1 failed: {result_1}")
    if result_2.get("status") != "committed":
        raise SystemExit(f"Execution 2 failed: {result_2}")
    if result_3.get("status") != "committed":
        raise SystemExit(f"Execution 3 failed: {result_3}")

    state = reconstruct_state()
    print_state_summary(state)

    if state["total_executions"] != 3:
        raise SystemExit("Reconstruction failed: incorrect execution count")

    if not state["history"]:
        raise SystemExit("Reconstruction failed: empty history")

    hash1 = compute_state_hash(state)
    state_again = reconstruct_state()
    hash2 = compute_state_hash(state_again)

    print("STATE HASH 1:", hash1)
    print("STATE HASH 2:", hash2)

    if hash1 != hash2:
        raise SystemExit("State hash mismatch: non-deterministic reconstruction")

    print("State reconstruction successful.")


if __name__ == "__main__":
    main()
