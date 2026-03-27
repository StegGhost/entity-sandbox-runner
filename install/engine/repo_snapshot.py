import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
SNAPSHOT_PATH = BRAIN_REPORTS / "repo_snapshot.json"

FAILED_DIR = ROOT / "failed_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
INSTALLED_DIR = ROOT / "installed_bundles"


def list_zip_files(path: Path):
    if not path.exists():
        return []
    return sorted([p for p in path.glob("*.zip") if p.is_file()])


def family_from_name(name: str) -> str:
    stem = Path(name).stem

    repaired_marker = "_repaired_"
    if repaired_marker in stem:
        stem = stem.split(repaired_marker)[0]

    parts = stem.split("_")
    while parts and (
        parts[-1].isdigit()
        or (parts[-1].startswith("v") and any(ch.isdigit() for ch in parts[-1]))
    ):
        parts.pop()

    return "_".join(parts) if parts else Path(name).stem


def latest_by_family(files):
    out = {}
    for f in files:
        fam = family_from_name(f.name)
        current = out.get(fam)
        if current is None or f.stat().st_mtime > current.stat().st_mtime:
            out[fam] = f
    return out


def serialize_file_map(file_map):
    result = {}
    for fam, path in sorted(file_map.items()):
        result[fam] = {
            "path": str(path),
            "mtime": path.stat().st_mtime,
            "name": path.name,
        }
    return result


def main():
    BRAIN_REPORTS.mkdir(parents=True, exist_ok=True)

    failed = list_zip_files(FAILED_DIR)
    repaired = list_zip_files(REPAIRED_DIR)
    incoming = list_zip_files(INCOMING_DIR)
    installed = list_zip_files(INSTALLED_DIR)

    failed_by_family = latest_by_family(failed)
    repaired_by_family = latest_by_family(repaired)
    incoming_by_family = latest_by_family(incoming)
    installed_by_family = latest_by_family(installed)

    snapshot = {
        "status": "ok",
        "generated_at": datetime.utcnow().isoformat(),
        "output": str(SNAPSHOT_PATH),
        "has_work": len(failed) > 0 or len(incoming) > 0,
        "incoming_bundle_count": len(incoming),
        "installed_bundle_count": len(installed),
        "failed_bundle_count": len(failed),
        "repaired_bundle_count": len(repaired),
        "family_counts": {
            "incoming_family_count": len(incoming_by_family),
            "installed_family_count": len(installed_by_family),
            "failed_family_count": len(failed_by_family),
            "repaired_family_count": len(repaired_by_family),
        },
        "latest_failed_by_family": serialize_file_map(failed_by_family),
        "latest_repaired_by_family": serialize_file_map(repaired_by_family),
        "latest_incoming_by_family": serialize_file_map(incoming_by_family),
        "latest_installed_by_family": serialize_file_map(installed_by_family),
    }

    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
