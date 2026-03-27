import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
BRAIN_REPORTS = ROOT / "brain_reports"

PREFLIGHT_INPUT = BRAIN_REPORTS / "headless_cmd_test.json"
PREFLIGHT_OUTPUT = BRAIN_REPORTS / "preflight_decision.json"


# -----------------------
# HELPERS
# -----------------------

def utc_ts():
    return datetime.utcnow().isoformat()


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


# -----------------------
# POLICY CONFIG (v1)
# -----------------------

CRITICAL_CHECKS = [
    "health",
    "token",
    "execute",
    "verify"
]

REPAIRABLE_CHECKS = [
    "health",     # network / service wake
    "token"       # retryable
]


# -----------------------
# EVALUATION LOGIC
# -----------------------

def evaluate_preflight(preflight: dict):
    result = {
        "ts": utc_ts(),
        "status": "failed",
        "decision": "reject_sandbox",
        "reason": None,
        "failed_checks": [],
        "repair_actions": [],
        "source": "preflight_gate"
    }

    if not preflight:
        result["reason"] = "missing_preflight_report"
        return result

    if preflight.get("status") != "ok":
        result["reason"] = "preflight_execution_failed"
        return result

    steps = preflight.get("steps", {})

    failed = []

    for check in CRITICAL_CHECKS:
        step = steps.get(check)

        if not step:
            failed.append(check)
            continue

        if not step.get("ok", False):
            failed.append(check)

    if not failed:
        result["status"] = "ok"
        result["decision"] = "run_experiment"
        result["reason"] = "all_critical_checks_passed"
        return result

    # -----------------------
    # HANDLE FAILURES
    # -----------------------

    result["failed_checks"] = failed

    # Determine if repairable
    repairable = []
    non_repairable = []

    for check in failed:
        if check in REPAIRABLE_CHECKS:
            repairable.append(check)
        else:
            non_repairable.append(check)

    if non_repairable:
        result["decision"] = "reject_sandbox"
        result["reason"] = "non_repairable_failures"
        return result

    # If all failures are repairable
    result["decision"] = "repair_sandbox"
    result["reason"] = "repairable_failures_detected"

    # Map simple repair actions (v1)
    actions = []

    for check in repairable:
        if check == "health":
            actions.append("retry_health_check")
        elif check == "token":
            actions.append("retry_token_request")

    result["repair_actions"] = actions

    return result


# -----------------------
# MAIN
# -----------------------

def main():
    preflight = load_json(PREFLIGHT_INPUT)

    decision = evaluate_preflight(preflight)

    write_json(PREFLIGHT_OUTPUT, decision)

    print(json.dumps({
        "status": "ok",
        "output": str(PREFLIGHT_OUTPUT),
        "decision": decision
    }, indent=2))


if __name__ == "__main__":
    main()
