
def test_integrity_stub():
    from engine.verify_signature import verify_signature
    result = verify_signature({"signature": {"key_id": "test"}})
    assert result["valid"]
