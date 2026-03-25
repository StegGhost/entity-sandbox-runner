from install.engine.admission_engine_v4 import admit_action

def test_admission_allowed():
    p = {"capabilities": ["COMM.EMAIL_SEND"]}
    state = {"hash": "abc"}
    res = admit_action(p, "SEND_EMAIL", state)
    assert res["allowed"] is True

def test_admission_rejected():
    p = {"capabilities": []}
    state = {"hash": "abc"}
    res = admit_action(p, "SEND_EMAIL", state)
    assert res["allowed"] is False
