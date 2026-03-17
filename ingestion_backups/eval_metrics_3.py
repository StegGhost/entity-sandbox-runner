metrics = []
def record(m): metrics.append(m)
def summary(): return {"count":len(metrics)}
