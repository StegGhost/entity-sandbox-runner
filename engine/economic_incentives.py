
from engine.consensus_engine import load_state
from engine.slashing_rewards import process_votes

def apply_incentives(bundle_hash, accepted):
    state = load_state()
    votes = state.get("votes", {}).get(bundle_hash, {})
    process_votes(bundle_hash, votes, accepted)
