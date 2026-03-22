from install.engine.execution_pipeline_v4 import execute_with_governance

def dummy_exec(action):
    return {"ok": True}

def test_execute():
    p = {"capabilities": ["COMM.EMAIL_SEND"], "agent": {"id": "x"}}
    state = {"hash": "abc"}
    res = execute_with_governance(p, "SEND_EMAIL", state, dummy_exec)
    assert res["status"] == "executed"
