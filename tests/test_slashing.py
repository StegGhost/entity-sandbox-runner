
from engine.slashing_rewards import reward, slash

def test_reward_slash():
    reward("nodeX", 1)
    slash("nodeX", 1)
