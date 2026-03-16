import sys
from pathlib import Path

# Ensure repo root is importable when run via GitHub Actions
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import zipfile
import shutil
import json
import subprocess
from datetime import datetime

from ingestion.enforce_capabilities import enforce_capabilities
from ingestion.classify_bundle_contents import classify_files
from ingestion.verify_installation import verify_against_manifest
from ingestion.write_install_report import write_install_report
from ingestion.move_processed_bundle import move_bundle
from ingestion.enforce_manifest import enforce_manifest
from ingestion.module_registry import record_install

# NEW: runtime capability validator
try:
    from ingestion.capability_validator import validate_capabilities
except Exception:
    validate_capabilities = None

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
                name = member.filename

                if name.endswith("/"):
                    continue

                p = Path(name)

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


def begin_transaction(bundle_path: str):

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


def finalize_transaction_success(tx_dir: Path):

    if tx_dir.exists():
        shutil.rmtree(tx_dir)

    tx_state = ROOT / "transaction_state.json"

    if tx_state.exists():
        tx_state.unlink()

    log("transaction completed successfully")


# NEW: run bundle installer if present
def run_bundle_installer(extracted_root: Path):

    installer_dir = extracted_root / "install"

    if not installer_dir.exists():
        return

    for installer in installer_dir.glob("*.py"):

        log(f"running bundle installer {installer}")

        subprocess.run(
            [sys.executable, str(installer)],
            cwd=ROOT,
            check=True
        )


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
            "verification": manifest_result,
            "moved_bundle_to": move_bundle(bundle_path, "failed"),
        }

        write_install_report(Path(bundle_path).name, report)

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
            "capabilities": capability_result,
            "moved_bundle_to": move_bundle(bundle_path, "failed"),
        }

        write_install_report(Path(bundle_path).name, report)

        cleanup_tmp()

        raise Exception(f"Capability enforcement failed: {capability_result}")

    normal_files = capability_result["filtered_normal_files"]
    workflow_files = capability_result["filtered_workflow_files"]

    # NEW: optional deep capability validator
    if validate_capabilities:
        validator = validate_capabilities(extracted, manifest)

        if not validator.get("verified", False):
            raise RuntimeError(
                f"Capability validator rejected bundle: {validator['violations']}"
            )

    if should_snapshot_runtime(normal_files):
        log("runtime-affecting bundle detected; creating runtime snapshot")
        snapshot_runtime()

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

        staged_verification = verify_against_manifest(tx_dir, extracted)

        if not staged_verification.get("verified", False):
            raise Exception(f"staged verification failed")

        installed_files = commit_transaction(tx_dir)

        finalize_transaction_success(tx_dir)

    except Exception:
        rollback_transaction(tx_dir)
        cleanup_tmp()
        raise

    # NEW: run smart installer
    run_bundle_installer(extracted)

    verification = verify_against_manifest(ROOT, extracted)

    status = "installed" if verification.get("verified", False) else "failed"

    moved_to = move_bundle(bundle_path, status)

    report = {
        "bundle_name": bundle_name,
        "bundle_version": bundle_version,
        "status": status,
        "installed_files_count": len(installed_files),
        "installed_files": installed_files,
        "verification": verification,
        "capabilities": capability_result,
        "moved_bundle_to": moved_to,
    }

    write_install_report(Path(bundle_path).name, report)

    record_install(bundle_name, bundle_version)

    log(f"safe ingestion complete status={status}")

    cleanup_tmp()

    return report


def main():

    if len(sys.argv) < 2:
        print("usage: python ingestion/runtime/ingest_engine.py <bundle_or_directory>")
        raise SystemExit(1)

    try:

        result = ingest_safe(sys.argv[1])

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:

        log(f"safe ingestion failed: {repr(e)}")

        cleanup_tmp()

        raise


if __name__ == "__main__":
    main()
