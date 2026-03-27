import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
REPO_SNAPSHOT_PATH = BRAIN_REPORTS / "repo_snapshot.json"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"

INCOMING_DIR = ROOT / "incoming_bundles"
FAILED_DIR = ROOT / "failed_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"
INSTALLED_DIR = ROOT / "installed_bundles"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def family_from_name(name: str) -> str:
    base = Path(name).stem

    suffixes = [
        "_manifest_fixed",
        "_repaired",
        "_bundle",
        "_v0_1",
        "_v0_2",
        "_v0_3",
        "_v0_4",
        "_v0_5",
        "_v0_6",
        "_v0_7",
        "_v0_8",
        "_v0_9",
        "_v1_0",
        "_v1_1",
        "_v1_2",
        "_v1_3",
        "_v1_4",
        "_v1_5",
        "_v1_6",
        "_v1_7",
        "_v1_8",
        "_v1_9",
        "_v2",
        "_v3",
        "_v4",
        "_v5",
        "_v6",
        "_v7",
        "_v8",
        "_v9",
        "_v10",
        "_v11",
        "_v12",
        "_v13",
        "_v14",
        "_v15",
        "_v16",
        "_v17",
        "_v18",
        "_v19",
        "_v20",
        "_v21",
        "_v22",
        "_v23",
        "_v24",
        "_v25",
        "_v26",
        "_v27",
        "_v28",
        "_v29",
        "_v30",
    ]

    for suffix in suffixes:
        if base.endswith(suffix):
            return base[: -len(suffix)]

    parts = base.split("_")
    if len(parts) >= 2 and parts[-1].startswith("v") and parts[-1][1:].replace("_", "").isdigit():
        return "_".join(parts[:-1])

    return base


def newest_zip_by_mtime(directory: Path):
    if not directory.exists():
        return []
    return sorted(directory.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)


def collect_family_index(directory: Path):
    families = {}
    for path in newest_zip_by_mtime(directory):
        fam = family_from_name(path.name)
        if fam not in families:
            families[fam] = {
                "path": str(path),
                "mtime": path.stat().st_mtime,
                "name": path.name,
                "family": fam,
            }
    return families


def same_family_installed(family: str) -> bool:
    if not INSTALLED_DIR.exists():
        return False
    for path in INSTALLED_DIR.glob("*.zip"):
        if family_from_name(path.name) == family:
            return True
    return False


def same_family_repaired(family: str) -> bool:
    if not REPAIRED_DIR.exists():
        return False
    for path in REPAIRED_DIR.glob("*.zip"):
        if family_from_name(path.name) == family:
            return True
    return False


def choose_incoming_action():
    incoming = newest_zip_by_mtime(INCOMING_DIR)
    if not incoming:
        return None

    target = incoming[0]
    family = family_from_name(target.name)

    return {
        "ts": datetime.utcnow().isoformat(),
        "status": "ok",
        "selection_mode": "incoming_priority",
        "active_family": family,
        "action": "inspect_incoming_bundle_family",
        "target": str(target),
        "family": family,
        "priority": "high",
        "reason": "incoming_bundle_detected",
        "source": "next_action_engine",
    }


def choose_failed_repair_action():
    failed = newest_zip_by_mtime(FAILED_DIR)
    if not failed:
        return None

    for target in failed:
        family = family_from_name(target.name)

        # Skip families that already have an installed or repaired representative.
        # This prevents thrashing on obsolete history.
        if same_family_installed(family):
            continue
        if same_family_repaired(family):
            continue

        return {
            "ts": datetime.utcnow().isoformat(),
            "status": "ok",
            "selection_mode": "repair_escalation",
            "active_family": family,
            "action": "propose_repair_for_bundle_family",
            "target": target.name,
            "family": family,
            "priority": "high",
            "reason": "failed_bundle_detected",
            "source": "next_action_engine",
        }

    return None


def choose_action(repo_snapshot: dict | None):
    if not repo_snapshot:
        return {
            "ts": datetime.utcnow().isoformat(),
            "status": "failed",
            "selection_mode": "none",
            "action": "idle",
            "reason": "missing_repo_snapshot",
            "source": "next_action_engine",
        }

    incoming_action = choose_incoming_action()
    if incoming_action:
        return incoming_action

    repair_action = choose_failed_repair_action()
    if repair_action:
        return repair_action

    return {
        "ts": datetime.utcnow().isoformat(),
        "status": "ok",
        "selection_mode": "none",
        "action": "idle",
        "reason": "no_actionable_work",
        "source": "next_action_engine",
    }


def main():
    repo_snapshot = load_json(REPO_SNAPSHOT_PATH)
    next_action = choose_action(repo_snapshot)

    payload = {
        "status": "ok" if next_action.get("status") == "ok" else "failed",
        "output": str(NEXT_ACTION_PATH),
        "next_action": next_action,
    }

    write_json(NEXT_ACTION_PATH, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
