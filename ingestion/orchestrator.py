import subprocess
from pathlib import Path

ROOT = Path.cwd()
INCOMING = ROOT / "incoming_bundles"


def log(msg):
    print(f"[orchestrator] {msg}")


def find_bundles():
    if not INCOMING.exists():
        return []
    return sorted(INCOMING.glob("*.zip"))


def run_safe_ingest(bundle):

    log(f"processing bundle {bundle}")

    cmd = [
        "python",
        "runtime_guardian.py",
        str(bundle)
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        log(f"bundle FAILED: {bundle}")
        return False

    log(f"bundle installed: {bundle}")
    return True


def run_workflow_review():

    review_dir = ROOT / "workflow_review"

    if not review_dir.exists():
        return

    for wf in review_dir.glob("*.yml"):
        log(f"workflow staged for manual review: {wf}")


def main():

    bundles = find_bundles()

    if not bundles:
        log("no bundles found")
        return

    log(f"{len(bundles)} bundle(s) detected")

    success = 0
    failed = 0

    for bundle in bundles:

        ok = run_safe_ingest(bundle)

        if ok:
            success += 1
        else:
            failed += 1

    run_workflow_review()

    log("orchestrator finished")
    log(f"successful bundles: {success}")
    log(f"failed bundles: {failed}")


if __name__ == "__main__":
    main()
