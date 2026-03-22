
from engine.authority_policy import is_authorized

def test_sdk_cannot_write_engine():
    ok, reason = is_authorized("install/engine/x.py", "sdk-key")
    assert ok is False

def test_admin_can_write_engine(monkeypatch):
    from engine import authority_policy

    def fake_role(key_id):
        return "admin"

    monkeypatch.setattr(authority_policy, "get_role_for_key", fake_role)

    ok, _ = is_authorized("install/engine/x.py", "admin-key")
    assert ok is True
