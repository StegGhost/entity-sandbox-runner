import os
import shutil

from governed_executor import execute_proposal, resolver


RECEIPT_DIR = "receipts"


def reset():
    if os.path.isdir(RECEIPT_DIR):
        shutil.rmtree(RECEIPT_DIR)


def demo_execute():
    return {
        "message": "hello from governed execution",
        "ok": True,
    }


def main():
    reset()

    resolver.register_authority(
        authority_id="local_admin",
        role="admin",
        trust_score=1.0,
    )

    proposal = {
        "name": "demo_proposal",
        "authority_id": "local_admin",
        "execute": demo_execute,
        "coherence": 1.0,
        "authority_validity": 1.0,
        "integrity": 1.0,
        "drift": 0.10,
        "resource_strain": 0.10,
        "entropy": 0.10,
    }

    result = execute_proposal(proposal)
    print(result)

    if result.get("status") != "committed":
        raise SystemExit(f"Validation failed: {result}")


if __name__ == "__main__":
    main()
