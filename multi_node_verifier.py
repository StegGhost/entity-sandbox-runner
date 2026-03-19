from state_reconstructor import reconstruct_state
from state_hash import compute_state_hash


def verify_multi_node_state(receipt_dir_a="receipts", receipt_dir_b="receipts"):
    state_a = reconstruct_state(receipt_dir=receipt_dir_a)
    state_b = reconstruct_state(receipt_dir=receipt_dir_b)

    hash_a = compute_state_hash(state_a)
    hash_b = compute_state_hash(state_b)

    return {
        "match": hash_a == hash_b,
        "hash_a": hash_a,
        "hash_b": hash_b,
        "state_a": state_a,
        "state_b": state_b,
    }
