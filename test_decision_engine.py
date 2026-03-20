from decision_engine import decide, execute_if_allowed


VALID_AUTH = {
    "valid": True,
    "authority_id": "local_admin",
    "authority": {"role": "admin", "trust_score": 1.0},
}

INVALID_AUTH = {
    "valid": False
}


def test_decision_allows_valid_execution():
    result = decide(
        proposal={"action": "test"},
        authority=VALID_AUTH
    )

    assert result["allowed"], "Expected decision to allow execution"


def test_decision_rejects_invalid_authority():
    result = decide(
        proposal={"action": "test"},
        authority=INVALID_AUTH
    )

    assert not result["allowed"], "Invalid authority should be rejected"


def test_execute_if_allowed_success():
    result = execute_if_allowed(
        proposal={"action": "test_exec"},
        authority=VALID_AUTH
    )

    assert result["status"] == "committed"


def test_execute_if_allowed_rejection():
    result = execute_if_allowed(
        proposal={"action": "test_exec"},
        authority=INVALID_AUTH
    )

    assert result["status"] == "rejected"
