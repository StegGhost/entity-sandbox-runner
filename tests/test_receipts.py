
def test_receipt_runs():
    from engine.governance_receipt import record_receipt
    record_receipt({"bundle_name":"x"}, "accepted", "test")
