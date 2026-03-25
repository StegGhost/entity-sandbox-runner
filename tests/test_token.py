
from engine.token_ledger import mint, get_balance

def test_token_flow():
    mint("nodeA", 50)
    assert get_balance("nodeA") >= 50
