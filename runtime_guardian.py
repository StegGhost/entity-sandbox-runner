import sys
import json
import zipfile
import shutil
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent

RUNTIME_FILES = [
    "ingestion/runtime/ingest_engine.py",
    "ingestion/enforce_manifest.py",
    "ingestion/classify_bundle_contents.py",
    "ingestion/verify_installation.py",
    "ingestion/write_install_report.py",
]

TRANSACTION_STATE = ROOT / "transaction_state.json"
TRANSACTION_STAGING = ROOT / "transaction_staging"


def runtime_intact():
    for rel in RUNTIME_FILES:
        if not (ROOT / rel).exists():
            return False
    return True


def restore_runtime():
    backup_dir = ROOT / "runtime_backups"
    backups = sorted(backup_dir.glob("runtime_*.zip"))

    if not backups:
        print("No runtime backup available")
        sys.exit(1)

    latest = backups[-1]

    with zipfile.ZipFile(latest) as z:
        z.extractall(ROOT)

    print(f"Runtime restored from backup: {latest}")


def transaction_incomplete():
    return TRANSACTION_STATE.exists() or TRANSACTION_STAGING.exists()


def recover_transaction():
    if TRANSACTION_STATE.exists():
        try:
            state = json.loads(TRANSACTION_STATE.read_text(encoding="utf-8"))
            print(f"Recovering incomplete transaction for bundle: {state.get('bundle', '<unknown>')}")
        except Exception:
            print("Recovering incomplete transaction: unreadable transaction_state.json")

    if TRANSACTION_STAGING.exists():
        shutil.rmtree(TRANSACTION_STAGING)
        print("Removed stale transaction_staging/")

    if TRANSACTION_STATE.exists():
        TRANSACTION_STATE.unlink()
        print("Removed stale transaction_state.json")


def main(bundle):
    if transaction_incomplete():
        print("Incomplete transaction detected — cleaning up before continuing")
        recover_transaction()

    if not runtime_intact():
        print("Runtime corrupted — restoring")
        restore_runtime()

    bootstrap = importlib.import_module("bootstrap_installer")
    bootstrap.main(bundle)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python runtime_guardian.py <bundle>")
        sys.exit(1)

    main(sys.argv[1])
