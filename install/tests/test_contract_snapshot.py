import json, os, tempfile
from install.engine.contract_snapshot import main

def test_snapshot_writes_file():
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "snap.json")
        main(path)
        assert os.path.exists(path)
        data = json.load(open(path, "r", encoding="utf-8"))
        assert "inferred_rules" in data
