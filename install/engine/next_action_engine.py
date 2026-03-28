import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FAILED_DIR = ROOT / "failed_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"
BRAIN_REPORTS = ROOT / "brain_reports"

OUTPUT_PATH = BRAIN_REPORTS / "next_action.json"


def now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def list_zip_files(path: Path):
    if not path.exists():
        return []
    return sorted(
        [p for p in path.iterdir() if p.is_file() and p.suffix.lower() == ".zip"],
        key=lambda p: p.name.lower(),
    )


def build_action() -> dict:
    failed = list_zip_files(FAILED_DIR)
    if failed:
        target = failed[0]
        return {
            "ts": now_ts(),
            "status": "ok",
            "selection_mode": "deterministic_failed_scan",
            "action_class": "repair",
            "action": "propose_repair_for_bundle_family",
            "target": str(target.resolve()),
            "family": target.stem,
            "priority": "high",
            "reason": "failed_bundle_present",
            "source": "next_action_engine",
        }

    repaired = list_zip_files(REPAIRED_DIR)
    if repaired:
        target = repaired[0]
        return {
            "ts": now_ts(),
            "status": "ok",
            "selection_mode": "deterministic_repaired_scan",
            "action_class": "repair",
            "action": "reintegrate_repaired_bundle",
            "target": str(target.resolve()),
            "family": target.stem,
            "priority": "high",
            "reason": "repaired_bundle_present",
            "source": "next_action_engine",
        }

    incoming = list_zip_files(INCOMING_DIR)
    if incoming:
        target = incoming[0]
        return {
            "ts": now_ts(),
            "status": "ok",
            "selection_mode": "deterministic_incoming_scan",
            "action_class": "inspection",
            "action": "inspect_incoming_bundle_family",
            "target": str(target.resolve()),
            "family": target.stem,
            "priority": "medium",
            "reason": "incoming_bundle_present",
            "source": "next_action_engine",
        }

    return {
        "ts": now_ts(),
        "status": "ok",
        "selection_mode": "idle",
        "action_class": "idle",
        "action": "idle",
        "target": "",
        "family": "none",
        "priority": "low",
        "reason": "no_work_available",
        "source": "next_action_engine",
    }


def main():
    next_action = build_action()
    payload = {
        "status": "ok",
        "output": str(OUTPUT_PATH),
        "next_action": next_action,
    }
    write_json(OUTPUT_PATH, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
