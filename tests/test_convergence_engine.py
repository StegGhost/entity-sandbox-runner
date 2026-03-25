from install.engine.closure_engine import (
    DEFAULT_STATE,
    compute_violations,
    compute_change_closure,
    converge,
)

def test_change_closure_expands_dependencies():
    closure = compute_change_closure(DEFAULT_STATE, "bundle_manifest")
    assert "bundle_manifest" in closure
    assert "receipts" in closure
    assert "feedback" in closure

def test_converge_reaches_zero_violations():
    history, state = converge()
    assert compute_violations(state) == []
    assert len(history) >= 2
