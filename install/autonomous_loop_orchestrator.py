import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BRAIN_REPORTS = ROOT / "brain_reports"

SNAPSHOT_FILE = BRAIN_REPORTS / "repo_snapshot.json"
NEXT_ACTION_FILE = BRAIN_REPORTS / "next_action.json"
PREFLIGHT_DECISION_FILE = BRAIN_REPORTS / "preflight_decision.json"


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


def semantic_route(preflight_decision: str, next_action_payload: dict | None):
    """
    Decide the execution lane from both sandbox admissibility and action semantics.

    Returns:
      run_experiment
      repair_sandbox
      inspect_sandbox
      reject_sandbox
      idle
      unknown
    """
    if preflight_decision != "run_experiment":
        return preflight_decision or "unknown"

    if not next_action_payload:
        return "unknown"

    next_action = next_action_payload.get("next_action", {})
    action = next_action.get("action")
    action_class = next_action.get("action_class", "idle")

    if action == "idle" or action_class == "idle":
        return "idle"

    if action_class == "repair":
        return "repair_sandbox"

    if action_class == "inspection":
        return "inspect_sandbox"

    if action_class == "experiment":
        return "run_experiment"

    return "unknown"


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
    # STEP 2: PREFLIGHT
    # -----------------
    preflight = run_step([
        "python",
        "install/engine/headless_cmd_tester.py",
        "--mode",
        "steggate_live_test"
    ])
    steps["preflight"] = preflight

    # -----------------
    # STEP 3: PREFLIGHT GATE
    # -----------------
    preflight_gate = run_step(["python", "install/engine/preflight_gate.py"])
    steps["preflight_gate"] = preflight_gate

    preflight_decision_payload = load_json(PREFLIGHT_DECISION_FILE)
    preflight_decision = None
    if preflight_decision_payload:
        preflight_decision = preflight_decision_payload.get("decision")

    steps["preflight_decision"] = preflight_decision_payload

    # -----------------
    # STEP 4: NEXT ACTION
    # -----------------
    next_action = run_step(["python", "install/engine/next_action_engine.py"])
    steps["next_action"] = next_action

    next_action_payload = load_json(NEXT_ACTION_FILE)
    steps["next_action_payload"] = next_action_payload

    routed_decision = semantic_route(preflight_decision, next_action_payload)
    steps["routed_decision"] = {
        "preflight_decision": preflight_decision,
        "routed_decision": routed_decision
    }

    # -----------------
    # STEP 5: ROUTING
    # -----------------
    if routed_decision == "run_experiment":
        execute = run_step(["python", "install/engine/execute_next_action.py"])
        steps["execute"] = execute

        reconcile = run_step(["python", "install/engine/reconcile_execution_state.py"])
        steps["reconcile"] = reconcile

    elif routed_decision == "repair_sandbox":
        repair = []

        # deterministic repair v1 only
        repair.append({
            "action": "rerun_repo_snapshot",
            "result": run_step(["python", "install/engine/repo_snapshot.py"])
        })
        repair.append({
            "action": "rerun_preflight",
            "result": run_step([
                "python",
                "install/engine/headless_cmd_tester.py",
                "--mode",
                "steggate_live_test"
            ])
        })
        repair.append({
            "action": "rerun_preflight_gate",
            "result": run_step(["python", "install/engine/preflight_gate.py"])
        })

        steps["repair"] = repair

    elif routed_decision == "inspect_sandbox":
        inspection = []

        # inspection lane is non-mutating
        inspection.append({
            "action": "inspection_no_mutation",
            "note": "inspection action acknowledged; no execution mutation performed"
        })

        steps["inspection"] = inspection

    elif routed_decision == "reject_sandbox":
        steps["reject"] = {
            "status": "blocked",
            "reason": "sandbox_not_admissible"
        }

    elif routed_decision == "idle":
        steps["idle"] = {
            "status": "ok",
            "reason": "no_experiment_action_selected"
        }

    else:
        steps["error"] = {
            "status": "failed",
            "reason": "unknown_or_missing_routed_decision"
        }

    total_duration = round(time.time() - loop_start, 3)

    output = {
        "status": "ok",
        "mode": "governed_autonomous_loop",
        "loop_ok": routed_decision == "run_experiment",
        "decision": routed_decision,
        "duration_seconds": total_duration,
        "steps": steps
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
