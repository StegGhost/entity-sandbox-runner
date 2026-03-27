import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
SNAPSHOT_PATH = BRAIN_REPORTS / "repo_snapshot.json"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def choose_action(snapshot: dict):
    if not snapshot:
        return {
            "ts": datetime.utcnow().isoformat(),
            "status": "failed",
            "selection_mode": "none",
            "action": "idle",
            "reason": "missing_repo_snapshot",
            "source": "next_action_engine",
        }

    failed_by_family = snapshot.get("latest_failed_by_family", {})
    repaired_by_family = snapshot.get("latest_repaired_by_family", {})
    incoming_by_family = snapshot.get("latest_incoming_by_family", {})

    # 1. Prefer incoming bundles that do not already have same-family installed/repaired dominance.
    # Keep this simple and conservative for now.
    for family, meta in sorted(incoming_by_family.items()):
        return {
            "ts": datetime.utcnow().isoformat(),
            "status": "ok",
            "selection_mode": "incoming_priority",
            "active_family": family,
            "action": "inspect_incoming_bundle_family",
            "target": meta["path"],
            "family": family,
            "priority": "high",
            "reason": "incoming_bundle_detected",
            "source": "next_action_engine",
        }

    # 2. Repair escalation with convergence lock:
    # do NOT re-repair a family if repaired artifact is newer than latest failed bundle.
    repair_candidates = []

    for family, failed_meta in failed_by_family.items():
        failed_mtime = failed_meta.get("mtime", 0)
        repaired_meta = repaired_by_family.get(family)

        if repaired_meta is not None:
            repaired_mtime = repaired_meta.get("mtime", 0)

            # convergence lock:
            # if repaired bundle is newer or equal, skip this family
            if repaired_mtime >= failed_mtime:
                continue

        repair_candidates.append(
            {
                "family": family,
                "target": failed_meta["path"],
                "failed_mtime": failed_mtime,
                "reason": "failed_bundle_without_newer_repair",
            }
        )

    if repair_candidates:
        repair_candidates.sort(key=lambda x: x["failed_mtime"], reverse=True)
        chosen = repair_candidates[0]

        return {
            "ts": datetime.utcnow().isoformat(),
            "status": "ok",
            "selection_mode": "repair_escalation",
            "active_family": chosen["family"],
            "action": "propose_repair_for_bundle_family",
            "target": chosen["target"],
            "family": chosen["family"],
            "priority": "high",
            "reason": chosen["reason"],
            "source": "repair_escalation",
        }

    # 3. Nothing admissible to do
    return {
        "ts": datetime.utcnow().isoformat(),
        "status": "ok",
        "selection_mode": "idle",
        "action": "idle",
        "reason": "no_admissible_work",
        "source": "next_action_engine",
    }


def main():
    snapshot = load_json(SNAPSHOT_PATH)
    next_action = choose_action(snapshot)

    payload = {
        "status": "ok" if next_action.get("status") == "ok" else "failed",
        "output": str(NEXT_ACTION_PATH),
        "next_action": next_action,
    }

    write_json(NEXT_ACTION_PATH, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
