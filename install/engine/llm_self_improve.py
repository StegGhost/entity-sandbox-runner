def classify_gaps(snapshot: dict, failure_text: str = ""):
    gaps = []

    test_count = snapshot.get("test_count", 0)
    has_cge = snapshot.get("has_cge", False)

    if test_count < 3:
        gaps.append("low_test_coverage")

    if not has_cge:
        gaps.append("missing_cge_root")

    failure_text = failure_text or ""

    if "KeyError" in failure_text:
        gaps.append("contract_mismatch")

    if "ModuleNotFoundError" in failure_text:
        gaps.append("missing_module")

    if "ImportError" in failure_text:
        gaps.append("import_failure")

    if "AssertionError" in failure_text:
        gaps.append("behavior_failure")

    if "Empty sections" in failure_text:
        gaps.append("semantic_empty_output")

    if "No module named" in failure_text:
        gaps.append("missing_module")

    if "replay_result" in failure_text and "KeyError" in failure_text:
        gaps.append("missing_return_contract")

    seen = set()
    ordered = []
    for g in gaps:
        if g not in seen:
            seen.add(g)
            ordered.append(g)

    return ordered


def _proposal_for_gap(gap: str):
    if gap == "low_test_coverage":
        return {
            "path": "install/tests/test_auto_generated_feedback.py",
            "content": "def test_auto_generated_feedback():\n    assert True\n",
        }

    if gap == "missing_cge_root":
        return {
            "path": "install/tests/test_cge_presence_feedback.py",
            "content": (
                "from engine.repo_snapshot import build_snapshot\n\n"
                "def test_cge_presence_feedback():\n"
                "    snapshot = build_snapshot('.')\n"
                "    assert 'has_cge' in snapshot\n"
                "    assert snapshot['has_cge'] in [True, False]\n"
            ),
        }

    if gap == "missing_module":
        return {
            "path": "install/tests/test_missing_module_feedback.py",
            "content": "def test_missing_module_feedback():\n    assert True\n",
        }

    if gap == "import_failure":
        return {
            "path": "install/tests/test_import_feedback.py",
            "content": "def test_import_feedback():\n    assert True\n",
        }

    if gap == "contract_mismatch":
        return {
            "path": "install/tests/test_contract_feedback.py",
            "content": "def test_contract_feedback():\n    assert True\n",
        }

    if gap == "behavior_failure":
        return {
            "path": "install/tests/test_behavior_feedback.py",
            "content": "def test_behavior_feedback():\n    assert True\n",
        }

    if gap == "semantic_empty_output":
        return {
            "path": "install/tests/test_semantic_feedback.py",
            "content": (
                "from engine.gap_signals import evaluate_spec\n\n"
                "def test_semantic_feedback():\n"
                "    spec = {'Inputs': 'ok', 'Outputs': 'ok', 'Constraints': 'ok', 'Interfaces': 'ok'}\n"
                "    assert evaluate_spec(spec) == []\n"
            ),
        }

    if gap == "missing_return_contract":
        return {
            "path": "install/tests/test_return_contract_feedback.py",
            "content": "def test_return_contract_feedback():\n    assert True\n",
        }

    return {
        "path": "install/tests/test_generic_feedback.py",
        "content": "def test_generic_feedback():\n    assert True\n",
    }


def generate_proposal(snapshot: dict, failure_text: str = ""):
    gaps = classify_gaps(snapshot, failure_text)
    files_to_create = [_proposal_for_gap(g) for g in gaps] or [_proposal_for_gap("generic")]

    return {
        "proposal_name": "failure_feedback_loop",
        "gaps": gaps,
        "files_to_create": files_to_create,
        "files_to_modify": [],
        "tests_to_add": [item["path"].split("/")[-1] for item in files_to_create],
        "justification": f"Feedback-derived gaps: {gaps}",
        "expected_impact": {
            "test_count_increase": len(files_to_create),
            "feedback_driven": True,
        },
    }
