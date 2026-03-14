from pathlib import Path
import difflib

repo_root = Path(".")
review_dir = repo_root / "workflow_review"
workflow_dir = repo_root / ".github/workflows"

for f in review_dir.glob("*.yml"):

    target = workflow_dir / f.name

    if not target.exists():
        print(f"NEW WORKFLOW: {f.name}")
        continue

    a = f.read_text().splitlines()
    b = target.read_text().splitlines()

    diff = list(difflib.unified_diff(b, a, fromfile="current", tofile="review"))

    if diff:
        print(f"\nDIFFERENT: {f.name}")
        for line in diff[:20]:
            print(line)
    else:
        print(f"SAME: {f.name}")
