import math

def compute_U(c, co, p, con):
    return (c * co) / max(p * con, 1e-9)

def margin(U):
    return math.log(U)

def classify(U):
    m = margin(U)
    if m > 1: return "healthy"
    if m > 0: return "caution"
    if m > -1: return "critical"
    return "unstable"
