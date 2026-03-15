import sys
from pathlib import Path

# Ensure repo root is importable when run via GitHub Actions
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import zipfile
import shutil
import json
from datetime import datetime

from ingestion.enforce_capabilities import enforce_capabilities
from ingestion.classify_bundle_contents import classify_files
from ingestion.verify_installation import verify_against_manifest
from ingestion.write_install_report import write_install_report
from ingestion.move_processed_bundle import move_bundle
from ingestion.enforce_manifest import enforce_manifest
from ingestion.module_registry import record_install

# Bootstrap-safe secure_extract import

# Bootstrap-safe secure_extract import
try:
    from ingestion.secure_extract import secure_extract_zip
except Exception:
    def secure_extract_zip(zip_path, dest):
        zip_path = Path(zip_path)
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path) as z:
            for member in z.infolist():
                member_name = member.filename

                # skip directory entries explicitly
                if member_name.endswith("/"):
                    continue

                p = Path(member_name)

                if p.is_absolute():
                    raise ValueError("absolute path in zip")

                if ".." in p.parts:
                    raise ValueError("zip path traversal detected")

                target = dest / p
                target.parent.mkdir(parents=True, exist_ok=True)

                with z.open(member, "r") as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)

        entries = [x for x in dest.iterdir()]
        if len(entries) == 1 and entries[0].is_dir():
            return entries[0]

        return dest

# Bootstrap-safe path_safety import
try:
    from ingestion.path_safety import validate_relative_path
except Exception:
    def validate_relative_path(p):
        p = Path(p)

        if p.is_absolute():
            raise ValueError("absolute paths not allowed")

        if ".." in p.parts:
            raise ValueError("path traversal not allowed")

        return p


ROOT = Path.cwd()
REPORT_DIR = ROOT / "ingestion_reports"
REPORT_DIR.mkdir(exist_ok=True)


def log(msg: str):
    ts = datetime.utcnow().isoformat()
    with open(REPORT_DIR / "ingestion.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)


def snapshot_runtime():
    backup_dir = ROOT / "runtime_backups"
    backup_dir.mkdir(exist_ok=True)

    name = datetime.utcnow().strftime("runtime_%Y%m%d_%H%M%S.zip")

    with zipfile.ZipFile(backup_dir / name, "w") as z:
        for p in (ROOT / "ingestion").rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(ROOT))

    log(f"runtime snapshot created: {backup_dir / name}")


def extract_if_zip(path: str) -> Path:
    p = Path(path)
    if p.suffix != ".zip":
        return p

    tmp = ROOT / "ingestion_tmp"
    extracted = secure_extract_zip(p, tmp)
    return extracted


def cleanup_tmp():
    tmp = ROOT / "ingestion_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
        log("cleaned ingestion_tmp")


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


def begin_transaction(bundle_path: str) -> Path:
    tx_dir = ROOT / "transaction_staging"
    if tx_dir.exists():
        shutil.rmtree(tx_dir)
    tx_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "active": True,
        "bundle": Path(bundle_path).name,
        "started_at": datetime.utcnow().isoformat()
    }

    (ROOT / "transaction_state.json").write_text(
        json.dumps(state, indent=2),
        encoding="utf-8"
    )

    log(f"transaction started for {Path(bundle_path).name}")
    return tx_dir


def stage_one(src: Path, rel: Path, tx_dir: Path):
    rel = validate_relative_path(rel)
    dest = tx_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    log(f"staged {dest}")
    return dest


def commit_transaction(tx_dir: Path):
    committed = []

    for p in tx_dir.rglob("*"):
        if not p.is_file():
            continue

        rel = p.relative_to(tx_dir)
        final_dest = ROOT / rel
        final_dest.parent.mkdir(parents=True, exist_ok=True)
        backup_file(final_dest)
        shutil.copy2(p, final_dest)
        committed.append(str(final_dest))
        log(f"committed {final_dest}")

    return committed


def rollback_transaction(tx_dir: Path):
    if tx_dir.exists():
        shutil.rmtree(tx_dir)
        log("transaction staging removed")

    tx_state = ROOT / "transaction_state.json"
    if tx_state.exists():
        tx_state.unlink()
        log("transaction state cleared")


def finalize_transaction_success():
    tx_state = ROOT / "transaction_state.json"
    if tx_state.exists():
        tx_state.unlink()
        log("transaction completed successfully")


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

        if ".." in safe_rel.parts or safe_rel.is_absolute():
            raise ValueError(f"unsafe workflow staging path: {safe_rel}")

        dest = review_root / safe_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        staged.append(str(dest))
        log(f"staged workflow for manual review {dest}")

    return staged


def install_bundle_readme(extracted_root: Path):
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


def should_snapshot_runtime(normal_files):
    for rel in normal_files:
        rel_str = str(rel).replace("\\", "/")
        if rel_str.startswith("ingestion/"):
            return True
    return False


def ingest_safe(bundle_path: str):
    print("Running safe ingestion from:", Path.cwd())

    extracted = extract_if_zip(bundle_path)
    log(f"extracted bundle root: {extracted}")

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
        cleanup_tmp()
        raise Exception(f"Manifest verification failed: {manifest_result}")

    manifest = manifest_result.get("manifest", {})
    bundle_name = manifest.get("bundle_name", Path(bundle_path).stem)
    bundle_version = manifest.get("version", "unknown")

    normal_files, workflow_files = classify_files(extracted)
    log(f"classified files: normal={len(normal_files)} workflow={len(workflow_files)}")

    capability_result = enforce_capabilities(
        manifest,
        normal_files,
        workflow_files
    )

    if not capability_result.get("verified", False):
        report = {
            "bundle_name": bundle_name,
            "bundle_version": bundle_version,
            "status": "failed",
            "installed_files_count": 0,
            "workflow_files_staged_count": 0,
            "installed_files": [],
            "workflow_review_files": [],
            "verification": manifest_result,
            "capabilities": capability_result,
            "moved_bundle_to": move_bundle(bundle_path, "failed"),
        }
        report_path = write_install_report(Path(bundle_path).name, report)
        log(f"capability enforcement failed; report written: {report_path}")
        cleanup_tmp()
        raise Exception(f"Capability enforcement failed: {capability_result}")

    normal_files = capability_result["filtered_normal_files"]
    workflow_files = capability_result["filtered_workflow_files"]

    if should_snapshot_runtime(normal_files):
        log("runtime-affecting bundle detected; creating runtime snapshot")
        snapshot_runtime()
    else:
        log("no runtime-affecting files detected; skipping runtime snapshot")

    tx_dir = begin_transaction(bundle_path)

    try:
        staged_files = []

        for rel in normal_files:
            rel = validate_relative_path(rel)
            src = extracted / rel

            if not src.exists():
                raise FileNotFoundError(f"missing source during staging: {src}")

            staged = stage_one(src, rel, tx_dir)
            staged_files.append(str(staged))

        # Verify the staged result before touching repo root
        staged_verification = verify_against_manifest(tx_dir, extracted)

        if not staged_verification.get("verified", False):
            raise Exception(f"staged verification failed: {staged_verification}")

        installed_files = commit_transaction(tx_dir)
        finalize_transaction_success()
        rollback_transaction(tx_dir)

    except Exception:
        rollback_transaction(tx_dir)
        cleanup_tmp()
        raise

    staged_workflows = stage_workflow_files(extracted, workflow_files)
    preserved_readme = install_bundle_readme(extracted)

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
        "staged_files_count": len(staged_files),
        "installed_files_count": len(installed_files),
        "workflow_files_staged_count": len(staged_workflows),
        "staged_files": staged_files,
        "installed_files": installed_files,
        "workflow_review_files": staged_workflows,
        "preserved_bundle_readme": preserved_readme,
        "staged_verification": staged_verification,
        "verification": verification,
        "capabilities": capability_result,
        "moved_bundle_to": moved_to,
    }

    report_path = write_install_report(Path(bundle_path).name, report)
    record_install(bundle_name, bundle_version)

    log(f"install report written: {report_path}")
    log(f"safe ingestion complete status={status}")
    cleanup_tmp()
    return report


def main():
    if len(sys.argv) < 2:
        print("usage: python ingestion/runtime/ingest_engine.py <bundle_or_directory>")
        raise SystemExit(1)

    try:
        result = ingest_safe(sys.argv[1])
        print(json.dumps(result, indent=2))
    except Exception as e:
        log(f"safe ingestion failed: {repr(e)}")
        cleanup_tmp()
        raise


if __name__ == "__main__":
    main()
