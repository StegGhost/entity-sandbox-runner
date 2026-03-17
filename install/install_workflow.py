import shutil
from pathlib import Path

ROOT = Path.cwd()
BUNDLE_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_SRC = BUNDLE_ROOT / "payload" / "workflows" / "run_experiment.yml"
WORKFLOW_DEST = ROOT / ".github" / "workflows" / "run_experiment.yml"

def main():
    WORKFLOW_DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(WORKFLOW_SRC, WORKFLOW_DEST)
    print("installed", WORKFLOW_DEST)

if __name__ == "__main__":
    main()
