
from engine.token_ledger import get_balance

def get_stake(node_id):
    return get_balance(node_id)
