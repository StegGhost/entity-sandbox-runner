import json
import hashlib
from pathlib import Path

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _pairwise(nodes):
    if len(nodes) % 2 == 1:
        nodes.append(nodes[-1])
    out = []
    for i in range(0, len(nodes), 2):
        out.append(sha256_bytes((nodes[i] + nodes[i+1]).encode("utf-8")))
    return out

def merkle_root_from_hashes(hashes):
    if not hashes:
        return None
    nodes = list(hashes)
    while len(nodes) > 1:
        nodes = _pairwise(nodes)
    return nodes[0]

def ledger_merkle_root(path: str):
    p = Path(path)
    hashes = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                hashes.append(obj["entry_hash"])
    return merkle_root_from_hashes(hashes)

if __name__ == "__main__":
    import sys
    print(ledger_merkle_root(sys.argv[1]))
