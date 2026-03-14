import subprocess
from pathlib import Path

def create_workflow_pr():

    review_dir = Path("workflow_review")

    if not review_dir.exists():
        return

    files = list(review_dir.glob("*.yml"))

    if not files:
        return

    subprocess.run([
        "gh",
        "pr",
        "create",
        "--title",
        "Promote staged workflows",
        "--body",
        "Auto-generated PR to promote staged workflows.",
        "--base",
        "main"
    ])
