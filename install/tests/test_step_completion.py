
from engine.step_completion import mark_completed_steps

def test_step_completion_runs():
    result = mark_completed_steps()
    assert "status" in result
