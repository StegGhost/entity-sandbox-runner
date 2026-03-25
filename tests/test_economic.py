
from engine.stake_registry import set_stake
from engine.consensus_engine import submit_vote
from engine.economic_consensus import weighted_tally

def test_weighted():
    set_stake("n1", 60)
    set_stake("n2", 60)

    submit_vote("h", "n1", "approve")
    submit_vote("h", "n2", "approve")

    result = weighted_tally("h", threshold=100)
    assert result["consensus"]
