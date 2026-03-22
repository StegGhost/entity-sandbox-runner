from pathlib import Path
import json
import hashlib
from datetime import datetime, timedelta


LOG_PATH = Path("logs/latest_failure.txt")
STATE_PATH = Path("logs/feedback_state.json")


def load_failure_text(path="logs/latest_failure.txt"):
    p = Path(path)
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def save_failure_text(text: str, path="logs/latest_failure.txt"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return str(p)


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_feedback_state():
    if not STATE_PATH.exists():
        return {
            "last_failure_hash": None,
            "last_bundle_path": None,
            "last_generated_at": None,
            "suppressed_count": 0,
        }
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {
            "last_failure_hash": None,
            "last_bundle_path": None,
            "last_generated_at": None,
            "suppressed_count": 0,
        }


def save_feedback_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def classify_failure_severity(failure_text: str) -> str:
    text = failure_text or ""

    if not text.strip():
        return "none"

    severe_markers = [
        "ModuleNotFoundError",
        "ImportError",
        "SyntaxError",
        "KeyError",
        "AssertionError",
        "FAILED",
        "ERROR",
    ]

    for marker in severe_markers:
        if marker in text:
            return "high"

    if "warning" in text.lower():
        return "low"

    return "medium"


def should_generate_feedback_bundle(
    failure_text: str,
    cooldown_minutes: int = 15,
):
    state = load_feedback_state()
    failure_hash = _hash_text(failure_text or "")
    severity = classify_failure_severity(failure_text)

    if severity == "none":
        return {
            "generate": False,
            "reason": "no_failure_text",
            "failure_hash": failure_hash,
            "severity": severity,
        }

    last_hash = state.get("last_failure_hash")
    last_generated_at = state.get("last_generated_at")

    if last_hash == failure_hash:
        return {
            "generate": False,
            "reason": "duplicate_failure",
            "failure_hash": failure_hash,
            "severity": severity,
        }

    if last_generated_at:
        try:
            last_dt = datetime.fromisoformat(last_generated_at)
            if datetime.utcnow() - last_dt < timedelta(minutes=cooldown_minutes):
                return {
                    "generate": False,
                    "reason": "cooldown_active",
                    "failure_hash": failure_hash,
                    "severity": severity,
                }
        except Exception:
            pass

    return {
        "generate": True,
        "reason": "new_failure",
        "failure_hash": failure_hash,
        "severity": severity,
    }


def record_feedback_bundle(bundle_path: str, failure_text: str):
    state = load_feedback_state()
    state["last_failure_hash"] = _hash_text(failure_text or "")
    state["last_bundle_path"] = bundle_path
    state["last_generated_at"] = datetime.utcnow().isoformat()
    save_feedback_state(state)
