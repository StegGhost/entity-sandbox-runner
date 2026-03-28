import json
import subprocess
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

SUMMARY_PATH = REPORTS / "loop_summary.json"
RECONCILE_PATH = REPORTS / "reconcile_result.json"
HEADLESS_PATH = REPORTS / "headless_cmd_test.json"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def fail(reason):
    payload = {
        "status": "rejected",
        "reason": reason,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    print(json.dumps(payload, indent=2))
    sys.exit(0)  # NOT failure → governance rejection


def main():
    summary = load_json(SUMMARY_PATH)
    reconcile = load_json(RECONCILE_PATH)
    headless = load_json(HEADLESS_PATH)

    if not summary or summary.get("status") != "ok":
        fail("loop_summary_not_ok")

    if not reconcile or reconcile.get("status") != "ok":
        fail("reconcile_not_ok")

    if not reconcile.get("reintegrated_ok"):
        fail("reintegrate_not_ok")

    # receipt optional (your current model allows this)
    # but enforce headless validation if present
    if headless:
        if headless.get("status") != "ok":
            fail("headless_failed")

        verify = headless.get("steps", {}).get("verify", {})
        if not verify.get("ok"):
            fail("receipt_verify_failed")

    # =========================
    # PROMOTION EXECUTION
    # =========================
    print("Promotion conditions passed. Promoting to main...")

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
        "reason": "admissibility_passed",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
    }, indent=2))


if __name__ == "__main__":
    main()
