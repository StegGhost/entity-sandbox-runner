import json
import os
import tempfile

from install.engine.bootstrap_permission_unlock import build_unlock_request, main

def test_build_unlock_request_contains_expected_fields():
    data = build_unlock_request()
    assert data["request_type"] == "permission_unlock"
    assert "docs/" in data["requested_allowed_paths"]
    assert "install/" in data["requested_allowed_paths"]

def test_main_writes_output_file():
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "out.json")
        main(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["next_bundle_expected"] == "sandbox_convergence_full_memory_bundle_v1"
