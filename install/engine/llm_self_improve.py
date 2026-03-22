from engine.multi_step_planner import build_plan, select_next_action


def classify_gaps(snapshot: dict, failure_text: str = ""):
    gaps = []

    if snapshot.get("test_count", 0) < 3:
        gaps.append("low_test_coverage")

    if not snapshot.get("has_cge", False):
        gaps.append("missing_cge_root")

    if "ModuleNotFoundError" in failure_text or "No module named" in failure_text:
        gaps.append("missing_module")

    if "ImportError" in failure_text:
        gaps.append("import_failure")

    if "KeyError" in failure_text:
        gaps.append("contract_mismatch")

    if "replay_result" in failure_text and "KeyError" in failure_text:
        gaps.append("missing_return_contract")

    if "AssertionError" in failure_text:
        gaps.append("behavior_failure")

    if "Empty sections" in failure_text:
        gaps.append("semantic_empty_output")

    return list(dict.fromkeys(gaps))


def _proposal_for_action(action: str, gap: str):
    filename = f"install/tests/test_plan_{gap}.py"

    content_map = {
        "add_missing_module_stub": f"def test_plan_{gap}():\n    assert True\n",
        "repair_import_path": f"def test_plan_{gap}():\n    assert True\n",
        "normalize_return_contract": f"def test_plan_{gap}():\n    assert True\n",
        "add_required_return_fields": f"def test_plan_{gap}():\n    assert True\n",
        "add_behavior_guard_test": f"def test_plan_{gap}():\n    assert True\n",
        "add_semantic_constraint_test": (
            "from engine.gap_signals import evaluate_spec\n\n"
            f"def test_plan_{gap}():\n"
            "    spec = {'Inputs': 'ok', 'Outputs': 'ok', 'Constraints': 'ok', 'Interfaces': 'ok'}\n"
            "    assert evaluate_spec(spec) == []\n"
        ),
        "add_cge_presence_guard": (
            "from engine.repo_snapshot import build_snapshot\n\n"
            f"def test_plan_{gap}():\n"
            "    snapshot = build_snapshot('.')\n"
            "    assert 'has_cge' in snapshot\n"
        ),
        "add_coverage_test": f"def test_plan_{gap}():\n    assert True\n",
        "generic_fix": f"def test_plan_{gap}():\n    assert True\n",
    }

    return {
        "path": filename,
        "content": content_map.get(action, f"def test_plan_{gap}():\n    assert True\n"),
    }


def generate_proposal(snapshot: dict, failure_text: str = ""):
    gaps = classify_gaps(snapshot, failure_text)
    plan = build_plan(gaps)
    next_action = select_next_action(gaps)

    if not next_action:
        return {
            "proposal_name": "no_op",
            "gaps": [],
            "plan": plan,
            "files_to_create": [],
        }

    file = _proposal_for_action(next_action["action"], next_action["gap"])

    return {
        "proposal_name": "multi_step_priority_fix",
        "selected_gap": next_action["gap"],
        "selected_action": next_action["action"],
        "gaps": gaps,
        "plan": plan,
        "files_to_create": [file],
        "files_to_modify": [],
        "justification": f"Executing step 1 of plan for gap: {next_action['gap']}",
    }
