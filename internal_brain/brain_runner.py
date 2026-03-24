import json
import traceback
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

# 🔑 CRITICAL FIX
sys.path.insert(0, str(ROOT))

REPORT_PATH = ROOT / "internal_brain" / "brain_report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def recent_files(rel_path: str, patterns: list[str], limit: int = 20) -> list[str]:
    base = ROOT / rel_path
    if not base.exists():
        return []

    found = []
    for pattern in patterns:
        found.extend([p for p in base.glob(pattern) if p.is_file()])

    found = sorted(set(found), key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p.relative_to(ROOT)) for p in found[:limit]]


def safe_read_json(rel_path: str):
    path = ROOT / rel_path
    if not path.exists() or not path.is_file():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_state() -> dict:
    state = {
        "ts": utc_now(),
        "root": str(ROOT),
        "paths": {
            "ingestion_reports": str(ROOT / "ingestion_reports"),
            "failed_bundles": str(ROOT / "failed_bundles"),
            "installed_bundles": str(ROOT / "installed_bundles"),
            "incoming_bundles": str(ROOT / "incoming_bundles"),
            "receipts": str(ROOT / "receipts"),
            "payload_feedback": str(ROOT / "payload" / "feedback"),
            "history_stream": str(ROOT / "history_stream.jsonl"),
        },
        "signals": {
            "recent_ingestion_reports": recent_files("ingestion_reports", ["*.json", "*.md", "*.log"]),
            "recent_failed_bundles": recent_files("failed_bundles", ["*.zip", "*.json"]),
            "recent_installed_bundles": recent_files("installed_bundles", ["*.zip", "*.json"]),
            "recent_incoming_bundles": recent_files("incoming_bundles", ["*.zip", "*.json"]),
            "recent_receipts": recent_files("receipts", ["*.json", "**/*.json"]),
            "recent_feedback": recent_files("payload/feedback", ["*.json", "*.md"]),
        },
        "samples": {},
    }

    if state["signals"]["recent_ingestion_reports"]:
        first = state["signals"]["recent_ingestion_reports"][0]
        if first.endswith(".json"):
            state["samples"]["latest_ingestion_report"] = safe_read_json(first)

    if state["signals"]["recent_feedback"]:
        for item in state["signals"]["recent_feedback"]:
            if item.endswith(".json"):
                state["samples"]["latest_feedback_json"] = safe_read_json(item)
                break

    return state


def load_modules():
    from internal_brain.internal_brain_explorer import explore
    from internal_brain.internal_brain_reconciler import reconcile
    from internal_brain.internal_brain_closure_engine import compute_closure
    from internal_brain.internal_brain_actuator import actuate

    return {
        "module_source": "internal_brain",
        "explore": explore,
        "reconcile": reconcile,
        "compute_closure": compute_closure,
        "actuate": actuate,
    }


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        state = build_state()
        modules = load_modules()

        explorer_output = modules["explore"](state)
        reconciler_output = modules["reconcile"](explorer_output, state)
        closure_output = modules["compute_closure"](reconciler_output, state)
        actuator_output = modules["actuate"](closure_output, state)

        report = {
            "ts": utc_now(),
            "report_version": "3.1",
            "module_source": modules["module_source"],
            "state": state,
            "explorer_output": explorer_output,
            "reconciler_output": reconciler_output,
            "closure_output": closure_output,
            "actuator_output": actuator_output,
            "summary": {
                "recent_failed_bundles": len(state["signals"]["recent_failed_bundles"]),
                "recent_incoming_bundles": len(state["signals"]["recent_incoming_bundles"]),
                "recent_installed_bundles": len(state["signals"]["recent_installed_bundles"]),
                "recent_ingestion_reports": len(state["signals"]["recent_ingestion_reports"]),
                "healthy": reconciler_output.get("healthy"),
                "proposed_actions": len(closure_output.get("actions", [])),
                "actuator_results": len(actuator_output.get("results", [])),
            },
        }

        with REPORT_PATH.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(str(REPORT_PATH))
        return 0

    except Exception as exc:
        error_report = {
            "ts": utc_now(),
            "report_version": "3.1",
            "status": "failed",
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }

        with REPORT_PATH.open("w", encoding="utf-8") as f:
            json.dump(error_report, f, indent=2)

        print(str(REPORT_PATH))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
