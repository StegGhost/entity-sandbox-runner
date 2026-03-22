
def test_multi_sig_structure():
    from engine.multi_sig_verify import verify_multi_signature
    result = verify_multi_signature({"signatures": []})
    assert result["valid"] is False
