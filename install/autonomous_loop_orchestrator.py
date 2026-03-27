import os
import json
import subprocess
import time

ROOT = os.getcwd()
REPORT_DIR = os.path.join(ROOT, "brain_reports")
os.makedirs(REPORT_DIR, exist_ok=True)


# -----------------------------
# UTIL
# -----------------------------

def now_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def run_step(cmd):
    start = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "raw_output": proc.stdout.strip(),
            "duration": round(time.time() - start, 3)
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": -1,
            "error": str(e),
            "duration": round(time.time() - start, 3)
        }


def safe_json_load(path):
    if not os.path.exists(path):
        return {}

    try:
        with open(path) as f:
            data = json.load(f)

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return {}

        return data if isinstance(data, dict) else {}

    except Exception:
        return {}


# -----------------------------
# CORE LOOP
# -----------------------------

def run_loop():
    start = time.time()

    result = {
        "status": "ok",
        "mode": "governed_autonomous_loop",
        "loop_ok": False,
        "decision": None,
        "duration_seconds": 0,
        "steps": {}
    }

    steps = {}

    # -----------------------------
    # 1. EXPLORE (repo snapshot)
    # -----------------------------
    explore = run_step([
        "python",
        "install/engine/repo_snapshot.py"
    ])
    steps["explore"] = explore

    snapshot = safe_json_load(
        os.path.join(REPORT_DIR, "repo_snapshot.json")
    )

    # -----------------------------
    # 2. PREFLIGHT (sandbox validation)
    # -----------------------------
    preflight = run_step([
        "python",
        "install/engine/preflight_gate.py"
    ])
    steps["preflight"] = preflight

    preflight_data = safe_json_load(
        os.path.join(REPORT_DIR, "preflight_decision.json")
    )

    preflight_decision = None
    if isinstance(preflight_data.get("decision"), dict):
        preflight_decision = preflight_data.get("decision", {}).get("decision")
    else:
        preflight_decision = preflight_data.get("decision")

    # -----------------------------
    # 3. NEXT ACTION
    # -----------------------------
    next_action = run_step([
        "python",
        "install/engine/next_action_engine.py"
    ])
    steps["next_action"] = next_action

    next_action_data = safe_json_load(
        os.path.join(REPORT_DIR, "next_action.json")
    )

    selected_next_action = next_action_data.get("next_action", {})
    action_class = selected_next_action.get("action_class")
    next_action_type = selected_next_action.get("action")

    # -----------------------------
    # 4. ROUTING DECISION
    # -----------------------------
    routed_decision = "inspect_sandbox"

    if preflight_decision == "repair_sandbox":
        routed_decision = "repair_sandbox"

    elif action_class == "inspection":
        routed_decision = "inspect_sandbox"

    elif action_class == "repair":
        routed_decision = "repair_sandbox"

    elif action_class == "execution" and preflight_decision == "run_experiment":
        routed_decision = "run_experiment"

    result["decision"] = routed_decision

    # -----------------------------
    # 5. EXECUTION ROUTES
    # -----------------------------

    if routed_decision == "inspect_sandbox":
        inspect = run_step([
            "python",
            "install/engine/inspect_bundle_engine.py",
            "--action-payload-json",
            json.dumps(selected_next_action)
        ])
        steps["inspect"] = inspect

    elif routed_decision == "repair_sandbox":
        repair = run_step([
            "python",
            "install/engine/repair_bundle_engine.py",
            "--action-payload-json",
            json.dumps(selected_next_action)
        ])
        steps["repair"] = repair

    elif routed_decision == "run_experiment":
        execute = run_step([
            "python",
            "install/engine/execute_next_action.py"
        ])
        steps["execute"] = execute

    # -----------------------------
    # 6. RECONCILE
    # -----------------------------
    reconcile = run_step([
        "python",
        "install/engine/reconcile_execution_state.py"
    ])
    steps["reconcile"] = reconcile

    # -----------------------------
    # FINALIZE
    # -----------------------------
    result["loop_ok"] = True
    result["duration_seconds"] = round(time.time() - start, 3)
    result["steps"] = steps

    output_path = os.path.join(REPORT_DIR, "loop_result.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


# -----------------------------
# ENTRY
# -----------------------------
if __name__ == "__main__":
    run_loop()
