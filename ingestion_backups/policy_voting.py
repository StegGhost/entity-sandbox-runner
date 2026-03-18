
def vote(actions):
    counts={}
    for a in actions:
        counts[a]=counts.get(a,0)+1
    return max(counts,key=counts.get)
