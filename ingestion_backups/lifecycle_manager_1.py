import hashlib
import json
import os
import shutil
import time
from typing import Dict, Any, Optional

from install.auth_scope import build_scope_record

CONTINUOUS_RECEIPTS_DIR = "payload/receipts"
CONTINUOUS_INTEGRITY_DIR = "payload/integrity"
STATE_FILE = "logs/state.json"
EXPERIMENT_ARCHIVE_ROOT = "archive/experiments"
REPLAY_ARCHIVE_ROOT = "archive/replays"

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def _safe_load_json(path: str) -> Optional[Dict[str, Any]]:
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return None
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def _safe_hash_path(path: str) -> Optional[str]:
    try:
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def _write_json(path: str, payload: Dict[str, Any]) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)

def _next_session_id(prefix: str) -> str:
    return f"{prefix}-{time.strftime('%Y%m%d')}-{int(time.time())}"

def _latest_receipt_hash() -> Optional[str]:
    if not os.path.exists(CONTINUOUS_RECEIPTS_DIR):
        return None
    files = sorted([f for f in os.listdir(CONTINUOUS_RECEIPTS_DIR) if f.endswith(".json")])
    if not files:
        return None
    latest = _safe_load_json(os.path.join(CONTINUOUS_RECEIPTS_DIR, files[-1]))
    if not latest:
        return None
    return latest.get("hash")

def _write_continuous_event(event_type: str, body: Dict[str, Any]) -> str:
    _ensure_dir(CONTINUOUS_RECEIPTS_DIR)
    files = sorted([f for f in os.listdir(CONTINUOUS_RECEIPTS_DIR) if f.endswith(".json")])
    idx = len(files) + 1
    payload = {
        "receipt_type": event_type,
        "timestamp": time.time(),
        "prev_hash": _latest_receipt_hash(),
    }
    payload.update(body)
    raw = json.dumps(payload, sort_keys=True).encode()
    payload["hash"] = hashlib.sha256(raw).hexdigest()
    path = os.path.join(CONTINUOUS_RECEIPTS_DIR, f"session_event_{idx:04d}.json")
    _write_json(path, payload)
    return path

def start_experiment(owner_id: str, experiment_name: str, visibility: str = "private_user_scoped",
                     auth_class: str = "experiment_content") -> Dict[str, Any]:
    exp_id = _next_session_id("EXP")
    exp_dir = os.path.join(EXPERIMENT_ARCHIVE_ROOT, build_scope_record(owner_id, visibility, auth_class)["owner_id_hash"], exp_id)
    _ensure_dir(exp_dir)

    snapshot = {
        "experiment_id": exp_id,
        "experiment_name": experiment_name,
        "started_at": time.time(),
        "state_hash": _safe_hash_path(STATE_FILE),
        "integrity_dir_hash": _safe_hash_path(os.path.join(CONTINUOUS_INTEGRITY_DIR, "")) if os.path.exists(CONTINUOUS_INTEGRITY_DIR) else None,
        "latest_receipt_hash": _latest_receipt_hash(),
    }
    scope = build_scope_record(owner_id, visibility, auth_class)

    manifest = {}
    manifest.update(snapshot)
    manifest.update(scope)

    _write_json(os.path.join(exp_dir, "manifest.json"), manifest)

    continuous_path = _write_continuous_event("experiment_start", {
        "experiment_id": exp_id,
        "experiment_name": experiment_name,
        **scope,
        "manifest_hash": _safe_hash_path(os.path.join(exp_dir, "manifest.json")),
        "state_hash": snapshot["state_hash"],
    })

    return {
        "experiment_id": exp_id,
        "archive_dir": exp_dir,
        "continuous_receipt": continuous_path,
    }

def end_experiment(owner_id_hash: str, experiment_id: str, result_summary: Dict[str, Any]) -> Dict[str, Any]:
    exp_dir = os.path.join(EXPERIMENT_ARCHIVE_ROOT, owner_id_hash, experiment_id)
    _ensure_dir(exp_dir)

    end_payload = {
        "experiment_id": experiment_id,
        "ended_at": time.time(),
        "end_state_hash": _safe_hash_path(STATE_FILE),
        "latest_receipt_hash": _latest_receipt_hash(),
        "result_summary": result_summary,
    }
    _write_json(os.path.join(exp_dir, "end_snapshot.json"), end_payload)

    continuous_path = _write_continuous_event("experiment_end", {
        "experiment_id": experiment_id,
        "owner_id_hash": owner_id_hash,
        "end_state_hash": end_payload["end_state_hash"],
        "latest_receipt_hash": end_payload["latest_receipt_hash"],
        "result_summary_hash": _safe_hash_path(os.path.join(exp_dir, "end_snapshot.json")),
    })

    return {
        "experiment_id": experiment_id,
        "archive_dir": exp_dir,
        "continuous_receipt": continuous_path,
    }

def start_replay(owner_id: str, source_experiment_id: str, visibility: str = "private_user_scoped",
                 auth_class: str = "replay_restricted") -> Dict[str, Any]:
    replay_id = _next_session_id("RPL")
    replay_dir = os.path.join(REPLAY_ARCHIVE_ROOT, build_scope_record(owner_id, visibility, auth_class)["owner_id_hash"], replay_id)
    _ensure_dir(replay_dir)

    scope = build_scope_record(owner_id, visibility, auth_class)
    manifest = {
        "replay_id": replay_id,
        "source_experiment_id": source_experiment_id,
        "started_at": time.time(),
        "state_hash": _safe_hash_path(STATE_FILE),
        "latest_receipt_hash": _latest_receipt_hash(),
        **scope,
    }
    _write_json(os.path.join(replay_dir, "manifest.json"), manifest)

    continuous_path = _write_continuous_event("replay_start", {
        "replay_id": replay_id,
        "source_experiment_id": source_experiment_id,
        **scope,
        "manifest_hash": _safe_hash_path(os.path.join(replay_dir, "manifest.json")),
    })

    return {
        "replay_id": replay_id,
        "archive_dir": replay_dir,
        "continuous_receipt": continuous_path,
    }

def end_replay(owner_id_hash: str, replay_id: str, summary: Dict[str, Any]) -> Dict[str, Any]:
    replay_dir = os.path.join(REPLAY_ARCHIVE_ROOT, owner_id_hash, replay_id)
    _ensure_dir(replay_dir)

    payload = {
        "replay_id": replay_id,
        "ended_at": time.time(),
        "latest_receipt_hash": _latest_receipt_hash(),
        "summary": summary,
    }
    _write_json(os.path.join(replay_dir, "replay_summary.json"), payload)

    continuous_path = _write_continuous_event("replay_end", {
        "replay_id": replay_id,
        "owner_id_hash": owner_id_hash,
        "summary_hash": _safe_hash_path(os.path.join(replay_dir, "replay_summary.json")),
        "latest_receipt_hash": payload["latest_receipt_hash"],
    })

    return {
        "replay_id": replay_id,
        "archive_dir": replay_dir,
        "continuous_receipt": continuous_path,
    }
