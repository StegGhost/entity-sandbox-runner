from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)

def test_propose_basic():
    r = client.post("/propose", json={
        "model_id": "gpt-test",
        "proposal_name": "api_test",
        "authority_id": "admin",
        "payload": {"x": 1}
    })

    assert r.status_code == 200
    assert "decision" in r.json()

def test_multi_llm_path():
    r = client.post("/propose", json={
        "variants": [
            {
                "proposal_name": "api_test",
                "authority_id": "admin",
                "payload": {"x": 1}
            },
            {
                "proposal_name": "api_test",
                "authority_id": "admin",
                "payload": {"x": 2}
            }
        ]
    })

    assert r.status_code == 200
