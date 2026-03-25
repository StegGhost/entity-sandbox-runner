
from engine.consensus_engine import submit_vote, tally_votes

def test_consensus_flow():
    submit_vote("abc", "node1", "approve")
    submit_vote("abc", "node2", "approve")
    result = tally_votes("abc", threshold=2)
    assert result["consensus"]
