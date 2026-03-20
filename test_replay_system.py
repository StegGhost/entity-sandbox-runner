from replay_engine import replay_chain
from invariant_checker import check_invariants
from receipt_chain_verifier import load_receipts


def test_replay_and_invariants():
    result = replay_chain("receipts")

    assert result["status"] == "ok"
    assert "final_state_hash" in result

    receipts = load_receipts("receipts")
    invariant_result = check_invariants(receipts)

    assert invariant_result["valid"] is True
