
from engine.core import SystemState, stability
from engine.consensus import is_network_stable

def test_network():
    s1 = SystemState(1,1,1,1)
    s2 = SystemState(0.5,1,1,1)
    scores = [stability(s1), stability(s2)]
    assert is_network_stable(scores) == False
