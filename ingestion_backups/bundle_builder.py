from pathlib import Path
from datetime import datetime
import shutil
import json

def build_bundle(results_file: str) -> str:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    root = Path("reproducibility") / f"experiment_{ts}"
    root.mkdir(parents=True, exist_ok=True)

    shutil.copy2(results_file, root / "dataset.json")
    meta = {"created_utc": datetime.utcnow().isoformat(), "results_file": results_file}
    (root / "config.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    if Path("receipts").exists():
        shutil.copytree("receipts", root / "receipts", dirs_exist_ok=True)

    (root / "README.md").write_text("Reproducibility Bundle\n\nRun local scripts against this dataset and receipts.\n", encoding="utf-8")
    (root / "reproduce_experiment.py").write_text("import json\nprint(json.load(open('config.json')))\nprint('Reproduction stub loaded')\n", encoding="utf-8")
    return str(root)
