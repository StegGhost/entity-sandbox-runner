import os
import shutil

from governed_executor import execute_proposal, resolver
from state_reconstructor import reconstruct_state, print_state_summary
from state_hash import compute_state_hash


RECEIPT_DIR = "receipts"


def demo_execute():
    return {"ok": True}


def make_proposal(name, authority_id="local_admin"):
    return {
        "name": name,
        "authority_id": authority_id,
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
    reset_environment()

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    resolver.register_authority(
        authority_id="backup_admin",
        role="admin",
        trust_score=0.9,
    )

    result_1 = execute_proposal(make_proposal("reconstruct_test_1", "local_admin"))
    result_2 = execute_proposal(make_proposal("reconstruct_test_2", "local_admin"))
    result_3 = execute_proposal(make_proposal("reconstruct_test_3", "backup_admin"))

    if result_1.get("status") != "committed":
        raise SystemExit(f"Execution 1 failed: {result_1}")
    if result_2.get("status") != "committed":
        raise SystemExit(f"Execution 2 failed: {result_2}")
    if result_3.get("status") != "committed":
        raise SystemExit(f"Execution 3 failed: {result_3}")

    state = reconstruct_state(RECEIPT_DIR)
    print_state_summary(state)

    if state["total_executions"] != 3:
        raise SystemExit("Reconstruction failed: incorrect execution count")

    if not state["history"]:
        raise SystemExit("Reconstruction failed: empty history")

    if "local_admin" not in state["authorities"]:
        raise SystemExit("Reconstruction failed: local_admin missing")

    if "backup_admin" not in state["authorities"]:
        raise SystemExit("Reconstruction failed: backup_admin missing")

    if not state["authority_drift_detected"]:
        raise SystemExit("Authority drift detection failed")

    hash1 = compute_state_hash(state)
    state_again = reconstruct_state(RECEIPT_DIR)
    hash2 = compute_state_hash(state_again)

    print("STATE HASH 1:", hash1)
    print("STATE HASH 2:", hash2)

    if hash1 != hash2:
        raise SystemExit("State hash mismatch: non-deterministic reconstruction")

    print("State reconstruction successful.")


if __name__ == "__main__":
    main()
