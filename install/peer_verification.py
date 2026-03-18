
def verify_peer_receipt(r):
    return "signature" in r and "hash" in r
