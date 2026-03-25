from install.engine.signed_receipts_v8 import create_signed_receipt, verify_signed_receipt

def test_signed_receipt():
    r = {"a":1}
    signed = create_signed_receipt(r)
    ok, reason = verify_signed_receipt(signed)
    assert ok is True

def test_missing_signature():
    r = {"a":1}
    ok, reason = verify_signed_receipt(r)
    assert ok is False
