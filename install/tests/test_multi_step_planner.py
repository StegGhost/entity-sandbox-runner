from engine.multi_step_planner import build_plan, select_next_action


def test_plan_orders_by_priority():
    gaps = ["low_test_coverage", "behavior_failure", "missing_module"]
    plan = build_plan(gaps)

    assert plan["ordered_gaps"][0] == "missing_module"
    assert plan["ordered_gaps"][1] == "behavior_failure"


def test_select_next_action():
    gaps = ["contract_mismatch", "low_test_coverage"]
    action = select_next_action(gaps)

    assert action["gap"] == "contract_mismatch"
    assert action["action"] == "normalize_return_contract"
