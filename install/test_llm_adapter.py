from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)


def test_propose_basic():
    client.post("/register_authority", params={
        "authority_id": "admin",
        "role": "system"
    })

    r = client.post("/propose", json={
        "model_id": "gpt-test",
        "proposal_name": "api_test",
        "authority_id": "admin",
        "payload": {"x": 1}
    })

    assert r.status_code == 200
    assert "decision" in r.json()
    assert "result" in r.json()


def test_multi_llm_path():
    client.post("/register_authority", params={
        "authority_id": "admin",
        "role": "system"
    })

    r = client.post("/propose_multi", json={
        "mode": "parallel",
        "proposals": [
            {
                "model_id": "gpt-test",
                "proposal_name": "api_test_a",
                "authority_id": "admin",
                "payload": {"x": 1}
            },
            {
                "model_id": "claude-test",
                "proposal_name": "api_test_b",
                "authority_id": "admin",
                "payload": {"x": 2}
            }
        ]
    })

    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "parallel"
    assert body["count"] == 2
    assert len(body["results"]) == 2


def test_signature_rejection():
    client.post("/register_authority", params={
        "authority_id": "admin",
        "role": "system"
    })

    r = client.post("/propose", json={
        "proposal_name": "api_test",
        "authority_id": "admin",
        "payload": {"x": 1},
        "signature": "bad_signature"
    })

    assert r.status_code == 200
    assert r.json()["allowed"] is False


def test_propose_multi_first_allowed():
    client.post("/register_authority", params={
        "authority_id": "admin",
        "role": "system"
    })

    r = client.post("/propose_multi", json={
        "mode": "first_allowed",
        "proposals": [
            {
                "model_id": "gpt-test",
                "proposal_name": "api_test_first",
                "authority_id": "admin",
                "payload": {"x": 1}
            },
            {
                "model_id": "claude-test",
                "proposal_name": "api_test_second",
                "authority_id": "admin",
                "payload": {"x": 2}
            }
        ]
    })

    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "first_allowed"
    assert "selected" in body


def test_propose_multi_majority():
    client.post("/register_authority", params={
        "authority_id": "admin",
        "role": "system"
    })

    r = client.post("/propose_multi", json={
        "mode": "majority",
        "proposals": [
            {
                "model_id": "gpt-test",
                "proposal_name": "api_test_m1",
                "authority_id": "admin",
                "payload": {"x": 1}
            },
            {
                "model_id": "claude-test",
                "proposal_name": "api_test_m2",
                "authority_id": "admin",
                "payload": {"x": 2}
            },
            {
                "model_id": "local-test",
                "proposal_name": "api_test_m3",
                "authority_id": "admin",
                "payload": {"x": 3}
            }
        ]
    })

    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "majority"
    assert body["count"] == 3
    assert "majority_allowed" in body
