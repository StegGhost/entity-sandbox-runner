from install.engine.receipt_chain import append_receipt, verify_chain

def test_chain_append_and_verify():
    # reset chain file
    import os
    if os.path.exists("receipt_chain.json"):
        os.remove("receipt_chain.json")

    append_receipt("abc", "SEND_EMAIL", {"ok": True})
    append_receipt("abc", "READ_EMAIL", {"ok": True})

    valid, reason = verify_chain()
    assert valid is True
