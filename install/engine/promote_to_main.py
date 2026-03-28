import subprocess
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def fail(reason):
    print(json.dumps({"status": "rejected", "reason": reason}, indent=2))
    sys.exit(0)


def main():
    # =========================
    # POLICY TOKEN
    # =========================
    if run(["python", "control_plane/tvc/issue_token.py"]).returncode != 0:
        fail("token_issue_failed")

    if run(["python", "control_plane/tvc/verify_token.py"]).returncode != 0:
        fail("token_invalid")

    # =========================
    # LOCAL SIGNED QUORUM
    # =========================
    if run(["python", "control_plane/tvc/check_signed_quorum.py"]).returncode != 0:
        fail("signed_quorum_failed")

    # =========================
    # DISTRIBUTED QUORUM
    # =========================
    if run(["python", "control_plane/tvc/check_distributed_quorum.py"]).returncode != 0:
        fail("distributed_quorum_failed")

    # =========================
    # RECEIPT VERIFICATION
    # =========================
    if run(["python", "control_plane/tc/verify_receipt.py"]).returncode != 0:
        fail("receipt_verification_failed")

    # =========================
    # GIT SAFE PROMOTION
    # =========================
    run(["git", "config", "user.name", "actions-user"])
    run(["git", "config", "user.email", "actions@github.com"])

    run(["git", "fetch", "origin", "main"])

    if run(["git", "rebase", "origin/main"]).returncode != 0:
        run(["git", "rebase", "--abort"])
        fail("rebase_failed")

    if run(["git", "push", "origin", "HEAD:main"]).returncode != 0:
        fail("push_failed")

    print(json.dumps({
        "status": "promoted",
        "mode": "distributed_signed_verified",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
    }, indent=2))


if __name__ == "__main__":
    main()
