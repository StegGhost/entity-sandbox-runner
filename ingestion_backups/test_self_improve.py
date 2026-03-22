from engine.repo_snapshot import build_snapshot
from engine.llm_self_improve import generate_proposal

def test_self_improve_v3():
    snap = build_snapshot()
    proposal = generate_proposal(snap)
    assert "files_to_create" in proposal
