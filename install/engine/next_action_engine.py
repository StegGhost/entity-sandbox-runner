import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
SNAPSHOT_PATH = BRAIN_REPORTS / "repo_snapshot.json"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
STATE_FILE = BRAIN_REPORTS / "loop_state.json"


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


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def build_idle(reason: str):
    return {
        "ts": datetime.utcnow().isoformat(),
        "status": "ok",
        "selection_mode": "idle",
        "action": "idle",
        "reason": reason,
        "source": "next_action_engine",
    }


def choose_incoming_candidate(snapshot: dict):
    incoming_by_family = snapshot.get("latest_incoming_by_family", {})
    if not incoming_by_family:
        return None

    candidates = []
    for family, meta in incoming_by_family.items():
        candidates.append(
            {
                "kind": "incoming",
                "family": family,
                "target": meta["path"],
                "mtime": meta.get("mtime", 0),
                "priority": "high",
                "selection_mode": "incoming_priority",
                "action": "inspect_incoming_bundle_family",
                "reason": "incoming_bundle_detected",
                "source": "next_action_engine",
            }
        )

    candidates.sort(key=lambda x: x["mtime"], reverse=True)
    return candidates[0]


def choose_repair_candidate(snapshot: dict):
    failed_by_family = snapshot.get("latest_failed_by_family", {})
    repaired_by_family = snapshot.get("latest_repaired_by_family", {})

    if not failed_by_family:
        return None

    candidates = []

    for family, failed_meta in failed_by_family.items():
        failed_mtime = failed_meta.get("mtime", 0)
        repaired_meta = repaired_by_family.get(family)

        # convergence lock:
        # skip any family already having a repaired artifact newer than the latest failure
        if repaired_meta is not None:
            repaired_mtime = repaired_meta.get("mtime", 0)
            if repaired_mtime >= failed_mtime:
                continue

        candidates.append(
            {
                "kind": "repair",
                "family": family,
                "target": failed_meta["path"],
                "mtime": failed_mtime,
                "priority": "high",
                "selection_mode": "repair_escalation",
                "action": "propose_repair_for_bundle_family",
                "reason": "failed_bundle_without_newer_repair",
                "source": "repair_escalation",
            }
        )

    if not candidates:
        return None

    candidates.sort(key=lambda x: x["mtime"], reverse=True)
    return candidates[0]


def apply_family_lock(chosen: dict | None):
    """
    Keep the loop from thrashing between families.
    If a different family is selected, hold the previous active family
    for up to 3 cycles, but only if that family still has admissible work.
    """
    if not chosen:
        state = load_state()
        state["active_family"] = None
        state["lock_count"] = 0
        state["last_action_kind"] = None
        save_state(state)
        return None

    state = load_state()
    last_family = state.get("active_family")
    last_kind = state.get("last_action_kind")
    lock_count = int(state.get("lock_count", 0))

    chosen_family = chosen.get("family")
    chosen_kind = chosen.get("kind")

    # reset lock if same family or no prior family
    if not last_family or last_family == chosen_family:
        state["active_family"] = chosen_family
        state["lock_count"] = 0
        state["last_action_kind"] = chosen_kind
        save_state(state)
        return chosen

    # only lock when the action kind stays the same
    if last_kind == chosen_kind and lock_count < 3:
        chosen["locked_from_family"] = last_family
        state["lock_count"] = lock_count + 1
        state["active_family"] = chosen_family
        state["last_action_kind"] = chosen_kind
        save_state(state)
        return chosen

    # release lock and accept new family
    state["active_family"] = chosen_family
    state["lock_count"] = 0
    state["last_action_kind"] = chosen_kind
    save_state(state)
    return chosen


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

    incoming_candidate = choose_incoming_candidate(snapshot)
    repair_candidate = choose_repair_candidate(snapshot)

    chosen = incoming_candidate or repair_candidate
    chosen = apply_family_lock(chosen)

    if not chosen:
        return build_idle("no_admissible_work")

    return {
        "ts": datetime.utcnow().isoformat(),
        "status": "ok",
        "selection_mode": chosen["selection_mode"],
        "active_family": chosen["family"],
        "action": chosen["action"],
        "target": chosen["target"],
        "family": chosen["family"],
        "priority": chosen["priority"],
        "reason": chosen["reason"],
        "source": chosen["source"],
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
