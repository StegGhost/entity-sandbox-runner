
from engine.priority_router import select_top_gap

def test_priority_selection():
    gaps = ["low_test_coverage", "missing_module"]
    top = select_top_gap(gaps)
    assert top == "missing_module"
