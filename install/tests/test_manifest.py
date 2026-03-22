
def test_manifest_paths():
    from install.engine.proposal_to_bundle import ALLOWED_PATHS
    assert "install/apply.py" in ALLOWED_PATHS
