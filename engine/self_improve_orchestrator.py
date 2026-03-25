import subprocess
import json
import os
from pathlib import Path

from engine.llm_self_improve import generate_proposal


REPORT_PATH = "brain_reports/self_improve_report.json"


def run_tests_capture():
    """Run pytest and capture output"""
    result = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        capture_output=True,
        text=True,
    )

    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def build_snapshot():
    """Minimal system snapshot (expand later)"""
    return {
        "test_count": count_tests(),
        "has_cge": os.path.exists("governed_executor.py"),
    }


def count_tests():
    total = 0
    for root, _, files in os.walk("."):
        for f in files:
            if f.startswith("test_") and f.endswith(".py"):
                total += 1
    return total


def apply_proposal(proposal: dict):
    files = proposal.get("files_to_create", [])

    for f in files:
        path = Path(f["path"])
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as fp:
            fp.write(f["content"])


def save_report(data: dict):
    Path("brain_reports").mkdir(exist_ok=True)

    with open(REPORT_PATH, "w") as f:
        json.dump(data, f, indent=2)


def run_self_improve_cycle():
    test_result = run_tests_capture()

    snapshot = build_snapshot()

    proposal = generate_proposal(
        snapshot,
        failure_text=test_result["stdout"] + test_result["stderr"],
    )

    applied = False

    if proposal.get("files_to_create"):
        apply_proposal(proposal)
        applied = True

    report = {
        "tests_passed": test_result["exit_code"] == 0,
        "exit_code": test_result["exit_code"],
        "gaps": proposal.get("gaps", []),
        "selected_gap": proposal.get("selected_gap"),
        "proposal": proposal,
        "applied": applied,
    }

    save_report(report)

    return report


if __name__ == "__main__":
    result = run_self_improve_cycle()
    print(json.dumps(result, indent=2))
