import shutil
import os

from governed_executor import execute_proposal, resolver
from state_reconstructor import reconstruct_state, print_state_summary


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

    execute_proposal(make_proposal("step_1"))
    execute_proposal(make_proposal("step_2"))
    execute_proposal(make_proposal("step_3"))

    state = reconstruct_state()

    print_state_summary(state)

    if state["total_executions"] != 3:
        raise SystemExit("Reconstruction failed: incorrect execution count")

    if not state["history"]:
        raise SystemExit("Reconstruction failed: empty history")

    print("State reconstruction successful.")


if __name__ == "__main__":
    main()
