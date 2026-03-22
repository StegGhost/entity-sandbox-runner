
def score_gaps(gaps):
    priority_order = {
        "missing_module": 100,
        "import_failure": 90,
        "contract_mismatch": 80,
        "missing_return_contract": 75,
        "behavior_failure": 70,
        "semantic_empty_output": 60,
        "missing_cge_root": 50,
        "low_test_coverage": 10,
    }

    scored = [(g, priority_order.get(g, 0)) for g in gaps]
    scored.sort(key=lambda x: x[1], reverse=True)

    return scored


def select_top_gap(gaps):
    scored = score_gaps(gaps)
    if not scored:
        return None
    return scored[0][0]
