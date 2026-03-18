import json, os

STATE_FILE = "payload/loop_state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"cycle": 0, "last_result": None}
    with open(STATE_FILE) as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def run_eval():
    try:
        from experiments.evaluation_suite.run_eval import main as eval_main
        return eval_main()
    except Exception as e:
        return {"error": str(e)}

def main():
    state = load_state()
    state["cycle"] += 1
    result = run_eval()
    state["last_result"] = result
    print(f"[V7] Cycle {state['cycle']} result:", result)
    save_state(state)

if __name__ == "__main__":
    main()
