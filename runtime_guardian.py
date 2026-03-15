import json
import sys
from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parent

RUNTIME_FILES = [
    "ingestion/ingest_bundle_safe.py",
    "ingestion/enforce_manifest.py",
    "ingestion/classify_bundle_contents.py",
]

def runtime_intact():

    for f in RUNTIME_FILES:
        if not (ROOT / f).exists():
            return False

    return True


def restore_runtime():

    backup_dir = ROOT / "runtime_backups"

    backups = sorted(backup_dir.glob("runtime_*.zip"))

    if not backups:
        print("No runtime backup available")
        sys.exit(1)

    latest = backups[-1]

    import zipfile

    with zipfile.ZipFile(latest) as z:
        z.extractall(ROOT)

    print("Runtime restored from backup:", latest)


def main(bundle):

    if not runtime_intact():
        print("Runtime corrupted — restoring")
        restore_runtime()

    bootstrap = importlib.import_module("bootstrap_installer")

    bootstrap.main(bundle)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: runtime_guardian.py <bundle>")
        sys.exit(1)

    main(sys.argv[1])
