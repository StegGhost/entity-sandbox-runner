
from install.engine.ui_api_adapter import format_dashboard

def test_ui():
    out = format_dashboard({}, {}, [])
    assert "metrics" in out
