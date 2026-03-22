
from dataclasses import dataclass

@dataclass
class SystemState:
    D: float
    M: float
    E: float
    A: float

def stability(state):
    if state.E * state.A == 0:
        return float("inf")
    return (state.D * state.M) / (state.E * state.A)
