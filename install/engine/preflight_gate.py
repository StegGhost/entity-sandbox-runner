import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRAIN_REPORTS = ROOT / "brain_reports"

OUTPUT_PATH = BRAIN_REPORTS / "preflight_decision.json"
HEADLESS_REPORT = BRAIN_REPORTS / "headless_cmd_test.json"
STRICT_LOG = ROOT / "logs" / "preflight.json"


def now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return None
        return data
    except Exception:
        return None


def run_step(cmd: list[str]):
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "duration": round(time.time() - start, 3)
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": round(time.time() - start, 3)
        }


def run_headless():
    step = run_step([
        "python",
        "install/engine/headless_cmd_tester.py",
        "--mode",
        "steggate_live_test"
    ])
    report = load_json(HEADLESS_REPORT)
    return step, report


def run_canonical():
    step = run_step([
        "python",
        "install/preflight_canonical.py"
    ])

    parsed = None
    if step["stdout"]:
        try:
            parsed = json.loads(step["stdout"])
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
        except Exception:
            parsed = None

    return step, parsed


def run_strict():
    step = run_step([
        "python",
        "install/preflight_strict.py"
    ])
    report = load_json(STRICT_LOG)
    return step, report


def evaluate_headless(report: dict | None):
    if not isinstance(report, dict):
        return {
            "status": "failed",
            "reason": "missing_headless_report",
            "repairable": True
        }

    if report.get("status") != "ok":
        return {
            "status": "failed",
            "reason": report.get("reason", "headless_failed"),
            "repairable": True
        }

    steps = report.get("steps", {})
    required = ["health", "token", "execute", "verify"]

    failed = []
    for key in required:
        step = steps.get(key)
        if not isinstance(step, dict) or not step.get("ok", False):
            failed.append(key)

    if failed:
        return {
            "status": "failed",
            "reason": "headless_runtime_checks_failed",
            "failed_checks": failed,
            "repairable": True
        }

    return {
        "status": "ok",
        "reason": "headless_pass"
    }


def evaluate_canonical(report: dict | None):
    if not isinstance(report, dict):
        return {
            "status": "failed",
            "reason": "missing_canonical_report",
            "repairable": True
        }

    status = report.get("status")
    repairs = report.get("repairs", [])
    drift = report.get("drift", [])

    if status == "pass":
        return {
            "status": "ok",
            "reason": "canonical_pass",
            "repairs": repairs,
            "drift_count": len(drift)
        }

    failed_drift = [
        d for d in drift
        if d.get("status") in {"missing_canonical", "missing_repo", "mismatch"}
    ]

    repairable = any(
        d.get("status") in {"missing_repo", "mismatch"}
        for d in failed_drift
    )

    non_repairable = any(
        d.get("status") == "missing_canonical"
        for d in failed_drift
    )

    return {
        "status": "failed",
        "reason": "canonical_fail",
        "repairable": repairable and not non_repairable,
        "failed_drift": failed_drift,
        "repairs": repairs
    }


def evaluate_strict(report: dict | None, strict_step: dict):
    if isinstance(report, dict):
        if report.get("status") == "pass":
            return {
                "status": "ok",
                "reason": "strict_pass",
                "repaired": report.get("repaired", [])
            }

        return {
            "status": "failed",
            "reason": "strict_fail",
            "repairable": bool(report.get("repaired")),
            "missing": report.get("missing", []),
            "repaired": report.get("repaired", [])
        }

    if strict_step.get("ok"):
        return {
            "status": "ok",
            "reason": "strict_pass_no_report"
        }

    return {
        "status": "failed",
        "reason": "missing_strict_report",
        "repairable": False
    }


def combine_decision(headless_eval: dict, canonical_eval: dict, strict_eval: dict):
    evaluations = {
        "headless": headless_eval,
        "canonical": canonical_eval,
        "strict": strict_eval
    }

    failed = {
        name: ev for name, ev in evaluations.items()
        if ev.get("status") != "ok"
    }

    if not failed:
        return {
            "ts": now_ts(),
            "status": "ok",
            "decision": "run_experiment",
            "reason": "all_preflight_layers_passed",
            "failed_checks": [],
            "repair_actions": [],
            "source": "preflight_gate"
        }

    repairable_failures = []
    non_repairable_failures = []

    for name, ev in failed.items():
        if ev.get("repairable", False):
            repairable_failures.append(name)
        else:
            non_repairable_failures.append(name)

    if non_repairable_failures:
        return {
            "ts": now_ts(),
            "status": "failed",
            "decision": "reject_sandbox",
            "reason": "non_repairable_preflight_failures",
            "failed_checks": list(failed.keys()),
            "repair_actions": repairable_failures,
            "source": "preflight_gate"
        }

    return {
        "ts": now_ts(),
        "status": "failed",
        "decision": "repair_sandbox",
        "reason": "repairable_preflight_failures",
        "failed_checks": list(failed.keys()),
        "repair_actions": repairable_failures,
        "source": "preflight_gate"
    }


def main():
    headless_step, headless_report = run_headless()
    canonical_step, canonical_report = run_canonical()
    strict_step, strict_report = run_strict()

    headless_eval = evaluate_headless(headless_report)
    canonical_eval = evaluate_canonical(canonical_report)
    strict_eval = evaluate_strict(strict_report, strict_step)

    decision = combine_decision(
        headless_eval=headless_eval,
        canonical_eval=canonical_eval,
        strict_eval=strict_eval
    )

    payload = {
        "status": "ok",
        "output": str(OUTPUT_PATH),
        "decision": decision,
        "inputs": {
            "headless": {
                "step": headless_step,
                "report": headless_report,
                "evaluation": headless_eval
            },
            "canonical": {
                "step": canonical_step,
                "report": canonical_report,
                "evaluation": canonical_eval
            },
            "strict": {
                "step": strict_step,
                "report": strict_report,
                "evaluation": strict_eval
            }
        }
    }

    write_json(OUTPUT_PATH, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
