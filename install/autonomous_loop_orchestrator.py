import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BRAIN_REPORTS = ROOT / "brain_reports"

SNAPSHOT_FILE = BRAIN_REPORTS / "repo_snapshot.json"
PREFLIGHT_FILE = BRAIN_REPORTS / "headless_cmd_test.json"
PREFLIGHT_DECISION_FILE = BRAIN_REPORTS / "preflight_decision.json"


# -----------------------
# GENERIC RUNNER
# -----------------------

def run_step(cmd):
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT
        )
        duration = round(time.time() - start, 3)

        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "raw_output": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "duration": duration
        }

    except Exception as e:
        return {
            "ok": False,
            "returncode": 1,
            "raw_output": "",
            "stderr": str(e),
            "duration": 0
        }


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def ensure_snapshot_exists():
    return SNAPSHOT_FILE.exists()


# -----------------------
# MAIN LOOP
# -----------------------

def main():
    loop_start = time.time()

    steps = {}

    # -----------------
    # STEP 1: EXPLORE
    # -----------------
    explore = run_step(["python", "install/engine/repo_snapshot.py"])

    if not ensure_snapshot_exists():
        explore["ok"] = False
        explore["stderr"] = "repo_snapshot_not_created"

    steps["explore"] = explore

    # -----------------
    # STEP 2: PREFLIGHT DIAGNOSTICS
    # -----------------
    preflight = run_step([
        "python",
        "install/engine/headless_cmd_tester.py",
        "--mode",
        "steggate_live_test"
    ])

    steps["preflight"] = preflight

    # -----------------
    # STEP 3: PREFLIGHT DECISION (CGE)
    # -----------------
    preflight_gate = run_step([
        "python",
        "install/engine/preflight_gate.py"
    ])

    steps["preflight_gate"] = preflight_gate

    decision_payload = load_json(PREFLIGHT_DECISION_FILE)
    decision = None

    if decision_payload:
        decision = decision_payload.get("decision")

    steps["decision"] = decision_payload

    # -----------------
    # STEP 4: ROUTING
    # -----------------

    execute = None
    reconcile = None
    next_action = None

    if decision == "run_experiment":

        # -----------------
        # NEXT ACTION
        # -----------------
        next_action = run_step(["python", "install/engine/next_action_engine.py"])
        steps["next_action"] = next_action

        # -----------------
        # EXECUTE
        # -----------------
        execute = run_step(["python", "install/engine/execute_next_action.py"])
        steps["execute"] = execute

        # -----------------
        # RECONCILE
        # -----------------
        reconcile = run_step(["python", "install/engine/reconcile_execution_state.py"])
        steps["reconcile"] = reconcile

    elif decision == "repair_sandbox":

        # Minimal deterministic repair (v1)
        repair = []

        # Re-run snapshot as safe repair
        repair.append(run_step(["python", "install/engine/repo_snapshot.py"]))

        # Re-run preflight once
        repair.append(run_step([
            "python",
            "install/engine/headless_cmd_tester.py",
            "--mode",
            "steggate_live_test"
        ]))

        repair.append(run_step([
            "python",
            "install/engine/preflight_gate.py"
        ]))

        steps["repair"] = repair

    elif decision == "reject_sandbox":

        steps["reject"] = {
            "status": "blocked",
            "reason": "sandbox_not_admissible"
        }

    else:

        steps["error"] = {
            "status": "failed",
            "reason": "unknown_or_missing_decision"
        }

    # -----------------
    # FINAL OUTPUT
    # -----------------

    total_duration = round(time.time() - loop_start, 3)

    output = {
        "status": "ok",
        "mode": "governed_autonomous_loop",
        "loop_ok": decision == "run_experiment",
        "decision": decision,
        "duration_seconds": total_duration,
        "steps": steps
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
