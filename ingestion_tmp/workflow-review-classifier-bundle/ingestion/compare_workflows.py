from pathlib import Path
from datetime import datetime, timezone
import difflib
import shutil
import hashlib
import json

ROOT = Path.cwd()
REVIEW_DIR = ROOT / "workflow_review"
LIVE_DIR = ROOT / ".github" / "workflows"
REPLACE_DIR = ROOT / "workflow_replace"
DEPRECATED_DIR = ROOT / "workflow_deprecated"
REPORT_DIR = ROOT / "ingestion_reports"

REPLACE_DIR.mkdir(parents=True, exist_ok=True)
DEPRECATED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def file_meta(path: Path):
    stat = path.stat()
    return {
        "path": str(path),
        "mtime_epoch": stat.st_mtime,
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "size": stat.st_size,
    }

def classify_one(review_file: Path):
    live_file = LIVE_DIR / review_file.name
    review_text = review_file.read_text(encoding="utf-8", errors="replace")
    review_hash = sha256_text(review_text)

    if not live_file.exists():
        status = "replace"
        reason = "no_live_workflow_exists"
        live_text = ""
        live_hash = None
        live_info = None
    else:
        live_text = live_file.read_text(encoding="utf-8", errors="replace")
        live_hash = sha256_text(live_text)
        live_info = file_meta(live_file)

        if review_hash == live_hash:
            status = "deprecated"
            reason = "identical_to_live_workflow"
        else:
            review_info = file_meta(review_file)
            if review_info["mtime_epoch"] >= live_info["mtime_epoch"]:
                status = "replace"
                reason = "review_workflow_is_newer_or_changed"
            else:
                status = "deprecated"
                reason = "review_workflow_is_older_than_live_workflow"

    diff_lines = list(
        difflib.unified_diff(
            live_text.splitlines(),
            review_text.splitlines(),
            fromfile=f"live/{review_file.name}" if live_file.exists() else "live/<missing>",
            tofile=f"review/{review_file.name}",
            lineterm=""
        )
    )

    destination_root = REPLACE_DIR if status == "replace" else DEPRECATED_DIR
    moved_file = destination_root / review_file.name
    if moved_file.exists():
        moved_file.unlink()
    shutil.move(str(review_file), str(moved_file))

    diff_path = destination_root / f"{review_file.name}.diff.md"
    summary = {
        "workflow": review_file.name,
        "status": status,
        "reason": reason,
        "review": file_meta(moved_file),
        "live": live_info,
        "review_sha256": review_hash,
        "live_sha256": live_hash,
        "diff_line_count": len(diff_lines),
    }

    diff_md = []
    diff_md.append(f"# Workflow Comparison: {review_file.name}")
    diff_md.append("")
    diff_md.append(f"- Status: `{status}`")
    diff_md.append(f"- Reason: `{reason}`")
    diff_md.append(f"- Compared at UTC: `{datetime.now(timezone.utc).isoformat()}`")
    diff_md.append("")
    diff_md.append("## Metadata")
    diff_md.append("")
    diff_md.append("```json")
    diff_md.append(json.dumps(summary, indent=2))
    diff_md.append("```")
    diff_md.append("")
    diff_md.append("## Unified Diff")
    diff_md.append("")

    if diff_lines:
        diff_md.append("```diff")
        diff_md.extend(diff_lines)
        diff_md.append("```")
    else:
        diff_md.append("_No textual diff._")

    diff_path.write_text("\n".join(diff_md) + "\n", encoding="utf-8")

    return summary

def main():
    if not REVIEW_DIR.exists():
        print("workflow_review directory does not exist.")
        return

    workflow_files = sorted(REVIEW_DIR.glob("*.yml")) + sorted(REVIEW_DIR.glob("*.yaml"))
    if not workflow_files:
        print("No workflow review files found.")
        return

    results = []
    for wf in workflow_files:
        result = classify_one(wf)
        results.append(result)
        print(f"{wf.name}: {result['status']} ({result['reason']})")

    out = REPORT_DIR / "workflow_comparison_summary.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Summary written: {out}")

if __name__ == "__main__":
    main()
