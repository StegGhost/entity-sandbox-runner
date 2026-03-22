
from engine.multi_step_planner import build_plan
from engine.plan_memory import load_plan, save_plan, get_next_step


def generate_proposal(snapshot: dict, failure_text: str = ""):
    existing_plan = load_plan()

    if not existing_plan:
        from engine.multi_step_planner import classify_gaps
        gaps = classify_gaps(snapshot, failure_text)
        plan = build_plan(gaps)
        for step in plan["steps"]:
            step["completed"] = False
        save_plan(plan)
    else:
        plan = existing_plan

    next_step = get_next_step(plan)

    if not next_step:
        return {
            "proposal_name": "plan_complete",
            "files_to_create": [],
            "plan": plan,
        }

    gap = next_step["gap"]

    return {
        "proposal_name": "plan_step_execution",
        "selected_gap": gap,
        "selected_step": next_step["step"],
        "files_to_create": [{
            "path": f"install/tests/test_plan_step_{gap}.py",
            "content": f"def test_plan_step_{gap}():\n    assert True\n"
        }],
        "plan": plan,
    }
