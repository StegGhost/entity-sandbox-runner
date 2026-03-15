import subprocess
from pathlib import Path

ROOT = Path.cwd()
INCOMING = ROOT / "incoming_bundles"


def log(msg):
    print(f"[orchestrator] {msg}")


def find_bundles():
    return sorted(INCOMING.glob("*.zip"))


def run_safe_ingest(bundle):
    log(f"processing bundle {bundle}")

    cmd = [
        "python",
        "runtime_guardian.py",
        str(bundle)
    ]

    subprocess.run(cmd, check=True)


def run_workflow_review():
    review_dir = ROOT / "workflow_review"

    if not review_dir.exists():
        return

    for wf in review_dir.glob("*.yml"):
        log(f"workflow staged for review: {wf}")


def main():
    bundles = find_bundles()

    if not bundles:
        log("no bundles found")
        return

    log(f"{len(bundles)} bundle(s) detected")

    for bundle in bundles:
        run_safe_ingest(bundle)

    run_workflow_review()

    log("orchestrator run complete")


if __name__ == "__main__":
    main()
