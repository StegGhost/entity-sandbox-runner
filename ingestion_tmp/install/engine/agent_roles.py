def planner(state):
    return {
        "proposed_root_object": next(
            (name for name, obj in state["objects"].items() if obj["status"] != "ok"),
            None
        )
    }

def observer(state):
    return {
        "all_ok": all(obj["status"] == "ok" for obj in state["objects"].values())
    }

def executor(state, closure):
    for obj in closure:
        state["objects"][obj]["status"] = "ok"
    return state
