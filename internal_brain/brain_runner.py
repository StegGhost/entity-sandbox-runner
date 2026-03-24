import json
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


ROOT = Path(__file__).resolve().parent.parent
INTERNAL_BRAIN_DIR = ROOT / "internal_brain"
REPORT_PATH = INTERNAL_BRAIN_DIR / "brain_report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_read_json(path: Path) -> Optional[Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def safe_read_text(path: Path, limit: int = 20000) -> Optional[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > limit:
            return text[:limit] + "\n...[truncated]..."
        return text
    except Exception:
        return None


def find_recent_files(directory: Path, patterns: List[str], limit: int = 25) -> List[str]:
    if not directory.exists():
        return []

    matches: List[Path] = []
    for pattern in patterns:
        matches.extend(directory.glob(pattern))

    unique = {p.resolve(): p for p in matches if p.is_file()}
    ordered = sorted(unique.values(), key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p.relative_to(ROOT)) for p in ordered[:limit]]


def build_repo_state() -> Dict[str, Any]:
    ingestion_reports = ROOT / "ingestion_reports"
    failed_bundles = ROOT / "failed_bundles"
    installed_bundles = ROOT / "installed_bundles"
    incoming_bundles = ROOT / "incoming_bundles"
    receipts = ROOT / "receipts"
    payload_feedback = ROOT / "payload" / "feedback"
    history_stream = ROOT / "history_stream.jsonl"

    state: Dict[str, Any] = {
        "ts": utc_now(),
        "root": str(ROOT),
        "paths": {
            "ingestion_reports": str(ingestion_reports),
            "failed_bundles": str(failed_bundles),
            "installed_bundles": str(installed_bundles),
            "incoming_bundles": str(incoming_bundles),
            "receipts": str(receipts),
            "payload_feedback": str(payload_feedback),
            "history_stream": str(history_stream),
        },
        "signals": {
            "recent_ingestion_reports": find_recent_files(
                ingestion_reports, ["*.json", "*.md", "*.log"], limit=20
            ),
            "recent_failed_bundles": find_recent_files(failed_bundles, ["*.zip", "*.json"], limit=20),
            "recent_installed_bundles": find_recent_files(installed_bundles, ["*.zip", "*.json"], limit=20),
            "recent_incoming_bundles": find_recent_files(incoming_bundles, ["*.zip", "*.json"], limit=20),
            "recent_receipts": find_recent_files(receipts, ["**/*.json", "*.json"], limit=20),
            "recent_feedback": find_recent_files(payload_feedback, ["*.json", "*.md"], limit=20),
        },
        "samples": {},
    }

    # Pull a few directly useful samples
    if state["signals"]["recent_feedback"]:
        first_feedback = ROOT / state["signals"]["recent_feedback"][0]
        if first_feedback.suffix.lower() == ".json":
            state["samples"]["feedback_json"] = safe_read_json(first_feedback)
        else:
            state["samples"]["feedback_text"] = safe_read_text(first_feedback)

    if state["signals"]["recent_ingestion_reports"]:
        first_report = ROOT / state["signals"]["recent_ingestion_reports"][0]
        if first_report.suffix.lower() == ".json":
            state["samples"]["ingestion_report_json"] = safe_read_json(first_report)
        else:
            state["samples"]["ingestion_report_text"] = safe_read_text(first_report)

    if history_stream.exists():
        try:
            lines = history_stream.read_text(encoding="utf-8", errors="replace").splitlines()
            tail = lines[-20:]
            parsed_tail = []
            for line in tail:
                line = line.strip()
                if not line:
                    continue
                try:
                    parsed_tail.append(json.loads(line))
                except Exception:
                    parsed_tail.append({"raw": line})
            state["samples"]["history_tail"] = parsed_tail
        except Exception as exc:
            state["samples"]["history_tail_error"] = str(exc)

    return state


def fallback_explorer(state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mode": "fallback",
        "summary": "Explorer fallback used",
        "observations": [
            {
                "kind": "count",
                "name": "failed_bundles",
                "value": len(state["signals"].get("recent_failed_bundles", [])),
            },
            {
                "kind": "count",
                "name": "incoming_bundles",
                "value": len(state["signals"].get("recent_incoming_bundles", [])),
            },
            {
                "kind": "count",
                "name": "installed_bundles",
                "value": len(state["signals"].get("recent_installed_bundles", [])),
            },
            {
                "kind": "count",
                "name": "ingestion_reports",
                "value": len(state["signals"].get("recent_ingestion_reports", [])),
            },
        ],
    }


def fallback_reconciler(explorer_output: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    failed = state["signals"].get("recent_failed_bundles", [])
    incoming = state["signals"].get("recent_incoming_bundles", [])
    installed = state["signals"].get("recent_installed_bundles", [])
    reports = state["signals"].get("recent_ingestion_reports", [])

    findings: List[Dict[str, Any]] = []

    if failed:
        findings.append({
            "severity": "high",
            "type": "failed_bundles_present",
            "detail": f"{len(failed)} recent failed bundle artifacts detected",
            "evidence": failed[:5],
        })

    if incoming:
        findings.append({
            "severity": "medium",
            "type": "incoming_bundles_present",
            "detail": f"{len(incoming)} recent incoming bundles detected",
            "evidence": incoming[:5],
        })

    if not reports:
        findings.append({
            "severity": "high",
            "type": "missing_ingestion_reports",
            "detail": "No recent ingestion reports found",
            "evidence": [],
        })

    if installed:
        findings.append({
            "severity": "low",
            "type": "installed_bundles_present",
            "detail": f"{len(installed)} recent installed bundle artifacts detected",
            "evidence": installed[:5],
        })

    return {
        "mode": "fallback",
        "summary": "Reconciler fallback used",
        "findings": findings,
        "healthy": len([f for f in findings if f["severity"] == "high"]) == 0,
        "explorer_summary": explorer_output.get("summary"),
    }


def fallback_closure_engine(reconciled: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    actions: List[Dict[str, Any]] = []
    findings = reconciled.get("findings", [])

    for finding in findings:
        ftype = finding.get("type")
        if ftype == "failed_bundles_present":
            actions.append({
                "action": "inspect_failed_bundles",
                "priority": 1,
                "targets": state["signals"].get("recent_failed_bundles", [])[:5],
                "reason": finding.get("detail"),
            })
        elif ftype == "missing_ingestion_reports":
            actions.append({
                "action": "inspect_ingestion_pipeline_reporting",
                "priority": 1,
                "targets": ["ingestion_reports/"],
                "reason": finding.get("detail"),
            })
        elif ftype == "incoming_bundles_present":
            actions.append({
                "action": "correlate_incoming_with_reports",
                "priority": 2,
                "targets": state["signals"].get("recent_incoming_bundles", [])[:5],
                "reason": finding.get("detail"),
            })

    if not actions:
        actions.append({
            "action": "no_action_required",
            "priority": 99,
            "targets": [],
            "reason": "No actionable issues detected by fallback closure engine",
        })

    return {
        "mode": "fallback",
        "summary": "Closure engine fallback used",
        "actions": sorted(actions, key=lambda x: x["priority"]),
    }


def fallback_actuator(closure_output: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    actions = closure_output.get("actions", [])
    executed = []
    for action in actions:
        executed.append({
            "action": action.get("action"),
            "status": "proposed_only",
            "targets": action.get("targets", []),
            "reason": action.get("reason", ""),
        })
    return {
        "mode": "fallback",
        "summary": "Actuator fallback used (no mutation performed)",
        "results": executed,
    }


def import_module_function(module_name: str, candidates: List[str]) -> Optional[Callable[..., Any]]:
    try:
        module = __import__(f"internal_brain.{module_name}", fromlist=["*"])
    except Exception:
        return None

    for name in candidates:
        fn = getattr(module, name, None)
        if callable(fn):
            return fn
    return None


def call_stage(
    stage_name: str,
    module_name: str,
    candidates: List[str],
    fallback_fn: Callable[..., Any],
    *args: Any,
) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "stage": stage_name,
        "used_fallback": False,
        "callable_name": None,
        "ok": True,
        "output": None,
        "error": None,
    }

    fn = import_module_function(module_name, candidates)
    if fn is None:
        result["used_fallback"] = True
        result["callable_name"] = f"{fallback_fn.__name__} (fallback)"
        try:
            result["output"] = fallback_fn(*args)
        except Exception as exc:
            result["ok"] = False
            result["error"] = f"Fallback failed: {exc}"
        return result

    result["callable_name"] = fn.__name__
    try:
        output = fn(*args)
        # Normalize non-dict outputs
        if isinstance(output, dict):
            result["output"] = output
        else:
            result["output"] = {
                "raw_output": output,
                "note": "Callable returned non-dict output; wrapped for reporting",
            }
    except TypeError:
        # Try reduced signatures if modules aren't aligned yet
        try:
            output = fn(args[0])
            if isinstance(output, dict):
                result["output"] = output
            else:
                result["output"] = {
                    "raw_output": output,
                    "note": "Callable returned non-dict output; wrapped for reporting",
                }
        except Exception as exc:
            result["used_fallback"] = True
            result["callable_name"] = f"{fallback_fn.__name__} (fallback after callable error)"
            result["error"] = f"Callable failed: {exc}"
            try:
                result["output"] = fallback_fn(*args)
            except Exception as fallback_exc:
                result["ok"] = False
                result["error"] = f"{result['error']} | Fallback failed: {fallback_exc}"
    except Exception as exc:
        result["used_fallback"] = True
        result["callable_name"] = f"{fallback_fn.__name__} (fallback after callable error)"
        result["error"] = f"Callable failed: {exc}"
        try:
            result["output"] = fallback_fn(*args)
        except Exception as fallback_exc:
            result["ok"] = False
            result["error"] = f"{result['error']} | Fallback failed: {fallback_exc}"

    return result


def build_report() -> Dict[str, Any]:
    state = build_repo_state()

    explorer_stage = call_stage(
        "explorer",
        "explorer",
        ["explore", "run", "main", "analyze"],
        fallback_explorer,
        state,
    )
    explorer_output = explorer_stage["output"] or {}

    reconciler_stage = call_stage(
        "reconciler",
        "reconciler",
        ["reconcile", "run", "main", "analyze"],
        fallback_reconciler,
        explorer_output,
        state,
    )
    reconciler_output = reconciler_stage["output"] or {}

    closure_stage = call_stage(
        "closure_engine",
        "closure_engine",
        ["compute_closure", "run", "main", "close"],
        fallback_closure_engine,
        reconciler_output,
        state,
    )
    closure_output = closure_stage["output"] or {}

    actuator_stage = call_stage(
        "actuator",
        "actuator",
        ["actuate", "run", "main", "execute"],
        fallback_actuator,
        closure_output,
        state,
    )

    return {
        "ts": utc_now(),
        "root": str(ROOT),
        "report_version": "1.0",
        "state": state,
        "stages": {
            "explorer": explorer_stage,
            "reconciler": reconciler_stage,
            "closure_engine": closure_stage,
            "actuator": actuator_stage,
        },
        "summary": {
            "recent_failed_bundles": len(state["signals"].get("recent_failed_bundles", [])),
            "recent_incoming_bundles": len(state["signals"].get("recent_incoming_bundles", [])),
            "recent_installed_bundles": len(state["signals"].get("recent_installed_bundles", [])),
            "recent_ingestion_reports": len(state["signals"].get("recent_ingestion_reports", [])),
            "fallbacks_used": [
                name
                for name, stage in {
                    "explorer": explorer_stage,
                    "reconciler": reconciler_stage,
                    "closure_engine": closure_stage,
                    "actuator": actuator_stage,
                }.items()
                if stage.get("used_fallback")
            ],
        },
    }


def main() -> int:
    INTERNAL_BRAIN_DIR.mkdir(parents=True, exist_ok=True)

    try:
        report = build_report()
        with REPORT_PATH.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(str(REPORT_PATH))
        return 0
    except Exception as exc:
        error_report = {
            "ts": utc_now(),
            "report_version": "1.0",
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
