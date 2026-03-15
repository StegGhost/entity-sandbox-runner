import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import zipfile
import shutil
import json
from datetime import datetime

from ingestion.classify_bundle_contents import classify_files
from ingestion.verify_installation import verify_against_manifest
from ingestion.write_install_report import write_install_report
from ingestion.move_processed_bundle import move_bundle
from ingestion.enforce_manifest import enforce_manifest
from ingestion.module_registry import record_install

ROOT = Path.cwd()
REPORT_DIR = ROOT / "ingestion_reports"
REPORT_DIR.mkdir(exist_ok=True)


def log(msg: str):
    ts = datetime.utcnow().isoformat()
    with open(REPORT_DIR / "ingestion.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)


def extract_if_zip(path: str) -> Path:
    p = Path(path)

    if p.suffix != ".zip":
        return p

    tmp = ROOT / "ingestion_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(p) as z:
        z.extractall(tmp)

    # If the zip expands into exactly one top-level directory, use it.
    entries = [x for x in tmp.iterdir()]
    if len(entries) == 1 and entries[0].is_dir():
        return entries[0]

    return tmp


def backup_file(dest: Path):
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

        if not src.exists():
            log(f"missing source during normal install: {src}")
            continue

        copy_one(src, dest)
        installed.append(str(dest))

    return installed


def stage_workflow_files(extracted_root: Path, workflow_files):
    review_root = ROOT / "workflow_review"
    review_root.mkdir(parents=True, exist_ok=True)

    staged = []

    for rel in workflow_files:
        src = extracted_root / rel
        if not src.exists():
            log(f"missing source during workflow staging: {src}")
            continue

        rel_parts = rel.parts
        if len(rel_parts) >= 3 and rel_parts[0] == ".github" and rel_parts[1] == "workflows":
            safe_rel = Path(*rel_parts[2:])
        else:
            safe_rel = rel

        dest = review_root / safe_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        staged.append(str(dest))
        log(f"staged workflow for manual review {dest}")

    return staged


def install_bundle_readme(extracted_root: Path):
    """
    Optionally preserve bundle README at repo root only if it is named distinctly.
    Avoid overwriting the repo root README.md by default.
    """
    candidates = list(extracted_root.rglob("README.md"))
    if not candidates:
        return None

    bundle_docs = ROOT / "ingestion_reports" / "bundle_docs"
    bundle_docs.mkdir(parents=True, exist_ok=True)

    src = candidates[0]
    dest = bundle_docs / f"{extracted_root.name}_README.md"
    shutil.copy2(src, dest)
    log(f"preserved bundle readme {dest}")
    return str(dest)


def ingest_safe(bundle_path: str):
    print("Running safe ingestion from:", Path.cwd())

    extracted = extract_if_zip(bundle_path)
    log(f"extracted bundle root: {extracted}")

    # Enforce manifest before installation.
    manifest_result = enforce_manifest(extracted)
    if not manifest_result.get("verified", False):
        report = {
            "status": "failed",
            "installed_files_count": 0,
            "workflow_files_staged_count": 0,
            "installed_files": [],
            "workflow_review_files": [],
            "verification": manifest_result,
            "moved_bundle_to": move_bundle(bundle_path, "failed"),
        }
        report_path = write_install_report(Path(bundle_path).name, report)
        log(f"manifest enforcement failed; report written: {report_path}")
        raise Exception(f"Manifest verification failed: {manifest_result}")

    manifest = manifest_result.get("manifest", {})
    bundle_name = manifest.get("bundle_name", Path(bundle_path).stem)
    bundle_version = manifest.get("version", "unknown")

    normal_files, workflow_files = classify_files(extracted)
    log(f"classified files: normal={len(normal_files)} workflow={len(workflow_files)}")

    installed_files = install_normal_files(extracted, normal_files)
    staged_workflows = stage_workflow_files(extracted, workflow_files)
    preserved_readme = install_bundle_readme(extracted)

    # Repo-side verification after installation.
    verification = verify_against_manifest(ROOT, extracted)

    if not verification.get("verified", False):
        status = "failed"
    elif staged_workflows:
        status = "installed_with_manual_review"
    else:
        status = "installed"

    moved_to = move_bundle(bundle_path, status)

    report = {
        "bundle_name": bundle_name,
        "bundle_version": bundle_version,
        "status": status,
        "installed_files_count": len(installed_files),
        "workflow_files_staged_count": len(staged_workflows),
        "installed_files": installed_files,
        "workflow_review_files": staged_workflows,
        "preserved_bundle_readme": preserved_readme,
        "verification": verification,
        "moved_bundle_to": moved_to,
    }

    report_path = write_install_report(Path(bundle_path).name, report)

    # Record module install only after successful manifest enforcement.
    record_install(bundle_name, bundle_version)

    log(f"install report written: {report_path}")
    log(f"safe ingestion complete status={status}")

    return report


def main():
    if len(sys.argv) < 2:
        print("usage: python ingestion/ingest_bundle_safe.py <bundle_or_directory>")
        raise SystemExit(1)

    try:
        result = ingest_safe(sys.argv[1])
        print(json.dumps(result, indent=2))
    except Exception as e:
        log(f"safe ingestion failed: {repr(e)}")
        raise


if __name__ == "__main__":
    main()
