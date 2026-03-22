from pathlib import Path

from engine.repo_snapshot import build_snapshot
from engine.llm_self_improve import generate_proposal
from engine.proposal_to_bundle import proposal_to_bundle
from engine.self_improve_runner import run_self_improve

def test_self_improve_loop_v4():
    snapshot = build_snapshot()
    proposal = generate_proposal(snapshot, failure_text="AssertionError: sample")

    assert "files_to_create" in proposal
    assert "gaps" in proposal

    bundle_path = proposal_to_bundle(proposal, output_path="incoming_bundles/auto_bundle_v4_test.zip")
    assert Path(bundle_path).exists()

def test_self_improve_runner_v4():
    result = run_self_improve(".", failure_text="ModuleNotFoundError: sample")
    assert result["status"] == "ok"
    assert result["bundle_exists"] is True
