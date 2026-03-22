
from engine.step_completion import mark_completed_steps
from engine.repo_snapshot import build_snapshot
from engine.llm_self_improve import generate_proposal
from engine.proposal_to_bundle import proposal_to_bundle


def run_self_improve(target_dir=".", failure_text=""):
    mark_completed_steps()

    snapshot = build_snapshot(target_dir)

    proposal = generate_proposal(snapshot, failure_text=failure_text)

    if not proposal.get("files_to_create"):
        return {"status": "no_op", "proposal": proposal}

    bundle_path = proposal_to_bundle(
        proposal,
        output_path="incoming_bundles/auto_bundle_feedback.zip",
    )

    return {
        "status": "ok",
        "bundle_path": bundle_path,
        "proposal": proposal,
    }


if __name__ == "__main__":
    print(run_self_improve())
