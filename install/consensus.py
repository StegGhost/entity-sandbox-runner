def consensus(results):
    votes = {"ok": 0, "fail": 0}
    for r in results:
        votes[r["decision"]] += 1
    return "ok" if votes["ok"] >= votes["fail"] else "fail"
