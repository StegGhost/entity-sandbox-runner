from install.engine.history_engine import record_bundle_result, read_history

def test_history_append():
    record_bundle_result("x", "failed", ["a"])
    history = read_history()
    assert len(history) >= 1
