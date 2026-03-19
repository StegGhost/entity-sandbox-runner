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

    resolver.register_authority("local_admin", "admin", 1.0)
    resolver.register_authority("backup_admin", "admin", 0.9)

    r1 = execute_proposal(make_proposal("test1", "local_admin"))
    r2 = execute_proposal(make_proposal("test2", "local_admin"))
    r3 = execute_proposal(make_proposal("test3", "backup_admin"))

    for i, r in enumerate([r1, r2, r3], start=1):
        if r.get("status") != "committed":
            raise SystemExit(f"Execution {i} failed: {r}")

    state = reconstruct_state(RECEIPT_DIR)
    print_state_summary(state)

    if state["total_executions"] != 3:
        raise SystemExit("Execution count mismatch")

    if not state["authority_drift_detected"]:
        raise SystemExit("Authority drift NOT detected")

    h1 = compute_state_hash(state)
    h2 = compute_state_hash(reconstruct_state(RECEIPT_DIR))

    print("STATE HASH 1:", h1)
    print("STATE HASH 2:", h2)

    if h1 != h2:
        raise SystemExit("Non-deterministic reconstruction")

    print("State reconstruction successful.")


if __name__ == "__main__":
    main()
