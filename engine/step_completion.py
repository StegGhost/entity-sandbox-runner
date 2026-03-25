
from pathlib import Path
from engine.plan_memory import load_plan, save_plan

def detect_completion():
    test_dir = Path("tests")
    if not test_dir.exists():
        return []

    completed = []
    for f in test_dir.glob("test_plan_step_*.py"):
        name = f.stem.replace("test_plan_step_", "")
        completed.append(name)
    return completed


def mark_completed_steps():
    plan = load_plan()
    if not plan:
        return {"status": "no_plan"}

    completed = detect_completion()

    updated = False
    for step in plan.get("steps", []):
        if step.get("gap") in completed and not step.get("completed"):
            step["completed"] = True
            updated = True

    if updated:
        save_plan(plan)

    return {
        "status": "updated" if updated else "no_change",
        "completed_detected": completed,
        "plan": plan
    }
