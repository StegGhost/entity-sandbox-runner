import json
import sys
from pathlib import Path

from engine.step_completion import mark_completed_steps
from engine.repo_snapshot import build_snapshot
from engine.llm_self_improve import generate_proposal
from engine.proposal_to_bundle import proposal_to_bundle


REPORT_PATH = Path("brain_reports/self_improve_result.json")


def _read_failure_text(argv) -> str:
    if len(argv) < 2:
        return ""

    path = Path(argv[1])
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8", errors="ignore")


def _write_report(payload: dict) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_self_improve(target_dir=".", failure_text=""):
    mark_completed_steps()

    snapshot = build_snapshot(target_dir)
    proposal = generate_proposal(snapshot, failure_text=failure_text)

    result = {
        "status": "no_op",
        "snapshot": snapshot,
        "proposal": proposal,
        "bundle_result": None,
    }

    if proposal.get("files_to_create"):
        bundle_result = proposal_to_bundle(
            proposal,
            output_path="incoming_bundles/auto_bundle_feedback.zip",
        )
        result["status"] = "ok"
        result["bundle_result"] = bundle_result

    _write_report(result)
    return result


if __name__ == "__main__":
    failure_text = _read_failure_text(sys.argv)
    print(json.dumps(run_self_improve(failure_text=failure_text), indent=2))
