from pathlib import Path

from engine.repo_snapshot import build_snapshot
from engine.llm_self_improve import generate_proposal
from engine.proposal_to_bundle import proposal_to_bundle
from engine.failure_feedback import save_failure_text, load_failure_text


def test_failure_feedback_bundle_generation():
    save_failure_text("AssertionError: sample failure")
    failure_text = load_failure_text()

    snapshot = build_snapshot()
    proposal = generate_proposal(snapshot, failure_text=failure_text)

    assert "behavior_failure" in proposal["gaps"] or "low_test_coverage" in proposal["gaps"]

    bundle_path = proposal_to_bundle(proposal, output_path="incoming_bundles/auto_bundle_feedback_test.zip")
    assert Path(bundle_path).exists()
