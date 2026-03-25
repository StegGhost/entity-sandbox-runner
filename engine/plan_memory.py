
from pathlib import Path
import json

STATE_PATH = Path("logs/plan_memory.json")


def load_plan():
    if not STATE_PATH.exists():
        return None
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return None


def save_plan(plan):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(plan, indent=2))


def get_next_step(plan):
    for step in plan.get("steps", []):
        if not step.get("completed"):
            return step
    return None


def mark_step_complete(plan, step_index):
    for step in plan.get("steps", []):
        if step.get("step") == step_index:
            step["completed"] = True
    save_plan(plan)
