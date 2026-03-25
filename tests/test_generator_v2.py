
from install.engine.proposal_to_bundle import normalize_allowed_paths

def test_install_scope():
    paths = normalize_allowed_paths("sample_bundle")
    assert "install/" in paths

def test_manifest_file():
    paths = normalize_allowed_paths("sample_bundle")
    assert "bundle_manifest.json" in paths
