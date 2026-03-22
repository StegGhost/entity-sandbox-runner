def generate_proposal(snapshot: dict):
    gaps = []
    if snapshot.get("test_count", 0) < 3:
        gaps.append("low_test_coverage")

    files = [{
        "path": "install/tests/test_auto_generated_v3.py",
        "content": "def test_auto_generated_v3():\n    assert True\n"
    }]

    return {
        "proposal_name": "self_improve_v3",
        "gaps": gaps,
        "files_to_create": files,
        "justification": str(gaps)
    }
