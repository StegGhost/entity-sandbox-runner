
def test_auto_repair():
    from install.engine.proposal_to_bundle import simulate_ingestion, auto_repair
    import tempfile, os, json

    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "install/tests"), exist_ok=True)
        os.makedirs(os.path.join(tmp, "install/engine"), exist_ok=True)

        manifest = {
            "bundle_name": "test",
            "bundle_version": "1.0.0",
            "install_mode": "folder_map",
            "allowed_paths": [
                "bundle_manifest.json",
                "install/tests/",
                "install/engine/",
                "install/apply.py"
            ]
        }

        with open(os.path.join(tmp, "bundle_manifest.json"), "w") as f:
            json.dump(manifest, f)

        # introduce violation
        bad_file = os.path.join(tmp, "bad.py")
        with open(bad_file, "w") as f:
            f.write("bad")

        ok, reason = simulate_ingestion(tmp)
        assert not ok

        auto_repair(tmp, reason)

        ok2, _ = simulate_ingestion(tmp)
        assert ok2
