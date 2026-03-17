def update_score(worker, success=True):
    if success:
        worker["score"] = worker.get("score",1)*1.05
    else:
        worker["score"] = worker.get("score",1)*0.9
    return worker
