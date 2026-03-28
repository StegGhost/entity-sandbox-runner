import json
import subprocess
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

SUMMARY = REPORTS / "loop_summary.json"
RECONCILE = REPORTS / "reconcile_result.json"
HEADLESS = REPORTS / "headless_cmd_test.json"


def load(path):
    try:
        return json.loads(path.read_text())
    except:
        return None


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def fail(reason):
    print(json.dumps({
        "status": "rejected",
        "reason": reason,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
    }, indent=2))
    sys.exit(0)


def require_tvc_token():
    issue = run(["python", "control_plane/tvc/issue_token.py"])
    if issue.returncode != 0:
        fail("tvc_issue_failed")

    verify = run(["python", "control_plane/tvc/verify_token.py"])
    if verify.returncode != 0:
        fail("tvc_verify_failed")


def main():
    summary = load(SUMMARY)
    reconcile = load(RECONCILE)
    headless = load(HEADLESS)

    if not summary or summary.get("status") != "ok":
        fail("loop_not_ok")

    if not reconcile or reconcile.get("status") != "ok":
        fail("reconcile_not_ok")

    if not reconcile.get("reintegrated_ok"):
        fail("reintegrate_not_ok")

    if headless:
        verify = headless.get("steps", {}).get("verify", {})
        if not verify.get("ok"):
            fail("receipt_verify_failed")

    # =========================
    # TVC AUTHORITY CHECK
    # =========================
    require_tvc_token()

    # =========================
    # PROMOTE
    # =========================
    run(["git", "config", "user.name", "actions-user"])
    run(["git", "config", "user.email", "actions@github.com"])

    run(["git", "fetch", "origin", "main"])

    rebase = run(["git", "rebase", "origin/main"])
    if rebase.returncode != 0:
        run(["git", "rebase", "--abort"])
        fail("rebase_failed")

    push = run(["git", "push", "origin", "HEAD:main"])
    if push.returncode != 0:
        fail("push_failed")

    print(json.dumps({
        "status": "promoted",
        "reason": "admissibility_and_authority_passed",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
    }, indent=2))


if __name__ == "__main__":
    main()
