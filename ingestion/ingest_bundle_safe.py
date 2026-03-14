import zipfile
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime

from ingestion.classify_bundle_contents import classify_files
from ingestion.verify_installation import verify_against_manifest, load_manifest
from ingestion.write_install_report import write_install_report
from ingestion.move_processed_bundle import move_bundle

ROOT = Path.cwd()
REPORT_DIR = ROOT / "ingestion_reports"
REPORT_DIR.mkdir(exist_ok=True)

def log(msg):
    ts = datetime.utcnow().isoformat()
    with open(REPORT_DIR / "ingestion.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)

def extract_if_zip(path):
    p = Path(path)
    if p.suffix != ".zip":
        return p

    tmp = ROOT / "ingestion_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(p) as z:
        z.extractall(tmp)

    return tmp

def backup_file(dest):
    if not dest.exists():
        return
    backup_dir = ROOT / "ingestion_backups"
    backup_dir.mkdir(exist_ok=True)
    target = backup_dir / dest.name
    counter = 1
    while target.exists():
        target = backup_dir / f"{dest.stem}_{counter}{dest.suffix}"
        counter += 1
    shutil.copy2(dest, target)

def copy_one(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    backup_file(dest)
    shutil.copy2(src, dest)
    log(f"installed {dest}")

def install_normal_files(extracted_root: Path, normal_files):
    installed = []
    for rel in normal_files:
        src = extracted_root / rel
        dest = ROOT / rel
        copy_one(src, dest)
        installed.append(str(dest))
    return installed

def stage_workflow_files(extracted_root: Path, workflow_files):
    review_root = ROOT / "workflow_review"
    review_root.mkdir(parents=True, exist_ok=True)
    staged = []

    for rel in workflow_files:
        src = extracted_root / rel
        safe_rel = Path(*rel.parts[2:]) if len(rel.parts) >= 3 and rel.parts[0] == ".github" and rel.parts[1] == "workflows" else rel
        dest = review_root / safe_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        staged.append(str(dest))
        log(f"staged workflow for manual review {dest}")

    return staged

def ingest_safe(bundle_path: str):
    extracted = extract_if_zip(bundle_path)
    normal_files, workflow_files = classify_files(extracted)

    installed_files = install_normal_files(extracted, normal_files)
    staged_workflows = stage_workflow_files(extracted, workflow_files)

    verification = verify_against_manifest(ROOT, extracted)

    if not verification["verified"]:
        status = "failed"
    elif staged_workflows:
        status = "installed_with_manual_review"
    else:
        status = "installed"

    moved_to = move_bundle(bundle_path, status)

    report = {
        "status": status,
        "installed_files_count": len(installed_files),
        "workflow_files_staged_count": len(staged_workflows),
        "installed_files": installed_files,
        "workflow_review_files": staged_workflows,
        "verification": verification,
        "moved_bundle_to": moved_to,
    }

    write_install_report(Path(bundle_path).name, report)
    log(f"safe ingestion complete status={status}")
    return report

def main():
    if len(sys.argv) < 2:
        print("usage: python ingestion/ingest_bundle_safe.py <bundle_or_directory>")
        raise SystemExit(1)

    result = ingest_safe(sys.argv[1])
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
