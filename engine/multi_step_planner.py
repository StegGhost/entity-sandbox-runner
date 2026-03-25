from engine.priority_router import score_gaps


def build_plan(gaps):
    scored = score_gaps(gaps)
    ordered = [gap for gap, _ in scored]

    plan = []
    for i, gap in enumerate(ordered, start=1):
        plan.append({
            "step": i,
            "gap": gap,
            "action": action_for_gap(gap),
        })

    return {
        "status": "ok",
        "gap_count": len(ordered),
        "ordered_gaps": ordered,
        "steps": plan,
    }


def action_for_gap(gap: str):
    mapping = {
        "missing_module": "add_missing_module_stub",
        "import_failure": "repair_import_path",
        "contract_mismatch": "normalize_return_contract",
        "missing_return_contract": "add_required_return_fields",
        "behavior_failure": "add_behavior_guard_test",
        "semantic_empty_output": "add_semantic_constraint_test",
        "missing_cge_root": "add_cge_presence_guard",
        "low_test_coverage": "add_coverage_test",
    }
    return mapping.get(gap, "generic_fix")


def select_next_action(gaps):
    plan = build_plan(gaps)
    if not plan["steps"]:
        return None
    return plan["steps"][0]
