def check_consensus(results):
    hashes = [r["result_hash"] for r in results]

    return len(set(hashes)) == 1
