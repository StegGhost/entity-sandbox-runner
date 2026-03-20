import time

from multi_node_verifier import verify_nodes
from node_recovery import recover_node
from receipt_gossip import gossip_receipts
from epoch_compactor import compact_epoch


NODES = ["receipts_node_a", "receipts_node_b"]
CANONICAL_NODE = "receipts_node_a"


def run_cycle():
    verification = verify_nodes(NODES)

    print("RUNTIME VERIFICATION:", verification)

    # 1. If consensus fails → recover bad nodes
    if not verification["consensus"]:
        for result in verification["results"]:
            if not result["valid"]:
                print(f"Recovering node: {result['node']}")
                recover_node(CANONICAL_NODE, result["node"])

    # 2. Gossip receipts (light propagation)
    gossip_receipts(NODES[0], NODES[1])
    gossip_receipts(NODES[1], NODES[0])

    # 3. Compact epochs (Merkle compression)
    for node in NODES:
        compact_epoch(node, epoch_size=5)


def run_autonomous_loop(interval=5):
    while True:
        run_cycle()
        time.sleep(interval)


if __name__ == "__main__":
    run_cycle()
