import subprocess
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def fail(reason):
    print(json.dumps({"status": "rejected", "reason": reason}, indent=2))
    sys.exit(0)


def main():
    # =========================
    # ISSUE TOKEN (policy)
    # =========================
    if run(["python", "control_plane/tvc/issue_token.py"]).returncode != 0:
        fail("token_issue_failed")

    # =========================
    # VERIFY TOKEN
    # =========================
    if run(["python", "control_plane/tvc/verify_token.py"]).returncode != 0:
        fail("token_invalid")

    # =========================
    # QUORUM CHECK
    # =========================
    if run(["python", "control_plane/tvc/check_quorum.py"]).returncode != 0:
        fail("quorum_failed")

    # =========================
    # RECEIPT BINDING
    # =========================
    if run(["python", "control_plane/tvc/bind_receipt.py"]).returncode != 0:
        fail("receipt_binding_failed")

    # =========================
    # GIT PROMOTION
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
        "reason": "policy_quorum_receipt_passed",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
    }, indent=2))


if __name__ == "__main__":
    main()
