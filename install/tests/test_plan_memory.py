
from engine.plan_memory import save_plan, load_plan, get_next_step

def test_plan_memory_cycle():
    plan = {
        "steps": [
            {"step": 1, "gap": "missing_module", "completed": False},
            {"step": 2, "gap": "behavior_failure", "completed": False}
        ]
    }

    save_plan(plan)
    loaded = load_plan()

    step = get_next_step(loaded)
    assert step["step"] == 1
