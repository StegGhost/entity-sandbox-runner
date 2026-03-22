from pathlib import Path

from engine.repo_snapshot import build_snapshot
from engine.llm_self_improve import generate_proposal
from engine.proposal_to_bundle import proposal_to_bundle
from engine.failure_feedback import (
    should_generate_feedback_bundle,
    record_feedback_bundle,
)


def run_self_improve(target_dir=".", failure_text=""):
    snapshot = build_snapshot(target_dir)

    decision = should_generate_feedback_bundle(failure_text)

    if not decision["generate"]:
        return {
            "status": "skipped",
            "reason": decision["reason"],
            "snapshot": snapshot,
            "failure_text": failure_text,
            "bundle_path": None,
            "bundle_exists": False,
        }

    proposal = generate_proposal(snapshot, failure_text=failure_text)
    bundle_path = proposal_to_bundle(
        proposal,
        output_path="incoming_bundles/auto_bundle_feedback.zip",
    )

    record_feedback_bundle(bundle_path, failure_text)

    return {
        "status": "ok",
        "reason": decision["reason"],
        "snapshot": snapshot,
        "proposal": proposal,
        "bundle_path": bundle_path,
        "bundle_exists": Path(bundle_path).exists(),
        "failure_text": failure_text,
    }


def main():
    result = run_self_improve(".", failure_text="")
    print(result)


if __name__ == "__main__":
    main()
