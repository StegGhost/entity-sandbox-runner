from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path.cwd()
BUNDLE_ROOT = Path(__file__).resolve().parents[1]

WORKFLOW_SRC = BUNDLE_ROOT / "payload" / "workflows" / "run_experiment.yml"

REVIEW_DIR = ROOT / "workflow_review"
REVIEW_DEST = REVIEW_DIR / "run_experiment.yml"
REVIEW_META = REVIEW_DIR / "run_experiment.review.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_backup(dest: Path):
    if not dest.exists():
        return None

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = dest.with_name(f"{dest.stem}.{stamp}{dest.suffix}.bak")
    shutil.copy2(dest, backup)
    return backup


def main():
    if not WORKFLOW_SRC.exists():
        raise FileNotFoundError(f"Missing workflow source: {WORKFLOW_SRC}")

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    backup_path = _safe_backup(REVIEW_DEST)
    shutil.copy2(WORKFLOW_SRC, REVIEW_DEST)

    review_record = {
        "status": "staged_for_manual_review",
        "reason": "GitHub blocks workflow writes from Actions without workflows permission",
        "source_workflow": str(WORKFLOW_SRC.relative_to(BUNDLE_ROOT)),
        "staged_workflow": str(REVIEW_DEST.relative_to(ROOT)),
        "intended_target": ".github/workflows/run_experiment.yml",
        "backup_created": str(backup_path.relative_to(ROOT)) if backup_path else None,
        "staged_at": _utc_now(),
        "next_step": "Copy staged file into .github/workflows/ manually"
    }

    REVIEW_META.write_text(json.dumps(review_record, indent=2), encoding="utf-8")

    print(f"Workflow staged at: {REVIEW_DEST}")
    print(f"Review metadata written: {REVIEW_META}")
    print("No direct modification to .github/workflows/ (safe mode)")


if __name__ == "__main__":
    main()
