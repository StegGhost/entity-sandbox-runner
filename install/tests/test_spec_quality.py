from engine.gap_signals import evaluate_spec


def test_spec_not_empty():
    spec = {
        "Inputs": "",
        "Outputs": "",
        "Constraints": "",
        "Interfaces": ""
    }

    failures = evaluate_spec(spec)

    assert len(failures) == 0, f"Empty sections: {failures}"
