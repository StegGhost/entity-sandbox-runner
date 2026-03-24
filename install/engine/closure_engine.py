import json
from copy import deepcopy

DEFAULT_STATE = {
    "objects": {
        "bundle_manifest": {
            "status": "stale",
            "depends_on": ["allowed_paths_policy", "tests", "receipts", "feedback"]
        },
        "allowed_paths_policy": {"status": "ok", "depends_on": []},
        "tests": {"status": "stale", "depends_on": []},
        "receipts": {"status": "stale", "depends_on": []},
        "feedback": {"status": "stale", "depends_on": ["receipts"]},
    }
}

def compute_violations(state):
    violations = []
    for name, data in state["objects"].items():
        if data["status"] != "ok":
            violations.append({
                "object": name,
                "status": data["status"]
            })
    return violations

def compute_change_closure(state, root_object):
    seen = set()
    order = []

    def visit(obj):
        if obj in seen:
            return
        seen.add(obj)
        order.append(obj)
        for dep in state["objects"][obj].get("depends_on", []):
            visit(dep)

    visit(root_object)
    return order

def apply_repair(state, root_object):
    closure = compute_change_closure(state, root_object)
    for obj in closure:
        state["objects"][obj]["status"] = "ok"
    return closure

def converge(initial_state=None):
    state = deepcopy(initial_state or DEFAULT_STATE)
    history = []

    while True:
        violations = compute_violations(state)
        history.append({
            "event_type": "scan",
            "violations": violations,
            "state": deepcopy(state)
        })
        if not violations:
            break

        root_object = violations[0]["object"]
        closure = apply_repair(state, root_object)
        history.append({
            "event_type": "repair",
            "root_object": root_object,
            "closure": closure,
            "state": deepcopy(state)
        })

    return history, state

def write_history(history, path="history_stream.jsonl"):
    with open(path, "w", encoding="utf-8") as f:
        for event in history:
            f.write(json.dumps(event) + "\n")

def main():
    history, state = converge()
    write_history(history)
    print(json.dumps({
        "final_violations": compute_violations(state),
        "final_state": state
    }, indent=2))

if __name__ == "__main__":
    main()
