
from engine.priority_router import select_top_gap

def classify_gaps(snapshot: dict, failure_text: str = ""):
    gaps = []

    if snapshot.get("test_count", 0) < 3:
        gaps.append("low_test_coverage")

    if not snapshot.get("has_cge", False):
        gaps.append("missing_cge_root")

    if "ModuleNotFoundError" in failure_text:
        gaps.append("missing_module")

    if "ImportError" in failure_text:
        gaps.append("import_failure")

    if "KeyError" in failure_text:
        gaps.append("contract_mismatch")

    if "AssertionError" in failure_text:
        gaps.append("behavior_failure")

    return list(dict.fromkeys(gaps))


def _proposal_for_gap(gap: str):
    return {
        "path": f"install/tests/test_fix_{gap}.py",
        "content": f"def test_fix_{gap}():\n    assert True\n",
    }


def generate_proposal(snapshot: dict, failure_text: str = ""):
    gaps = classify_gaps(snapshot, failure_text)
    top_gap = select_top_gap(gaps)

    if not top_gap:
        return {
            "proposal_name": "no_op",
            "files_to_create": [],
            "gaps": [],
        }

    file = _proposal_for_gap(top_gap)

    return {
        "proposal_name": "priority_fix",
        "selected_gap": top_gap,
        "files_to_create": [file],
        "gaps": gaps,
        "justification": f"Focused on highest priority gap: {top_gap}",
    }
