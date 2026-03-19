from state_reconstructor import reconstruct_state

RECEIPT_DIR = "receipts"


def main():
    state = reconstruct_state(RECEIPT_DIR)

    print("=== RECONSTRUCTED SYSTEM STATE ===")
    print(f"Total Executions: {state.get('count', 0)}")
    print(f"Last U: {state.get('last_u')}")

    decision = state.get("last_decision")
    print(f"Last Decision: {decision}")

    authorities = state.get("authorities", [])
    print(f"Authorities: {authorities}")

    assert state.get("state_hash_1") == state.get("state_hash_2")

    print("State reconstruction successful.")


if __name__ == "__main__":
    main()
