from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)


def test_full_flow():
    # register authority
    r = client.post("/register_authority", params={
        "authority_id": "admin",
        "role": "system"
    })
    assert r.status_code == 200

    payload = {
        "name": "api_test",
        "authority_id": "admin",
        "payload": {"x": 1}
    }

    # decision
    r = client.post("/decide", json=payload)
    assert r.status_code == 200
    assert r.json()["decision"]["allowed"]

    # execute
    r = client.post("/execute", json=payload)
    assert r.status_code == 200
    assert r.json()["result"]["status"] == "committed"
