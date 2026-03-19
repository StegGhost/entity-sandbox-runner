import shutil, os
from governed_executor import execute_proposal, resolver
from receipt_chain_verifier import clear_chain_lock
from state_reconstructor import reconstruct_state

def main():
    clear_chain_lock()
    shutil.rmtree("receipts", ignore_errors=True)
    os.makedirs("receipts", exist_ok=True)

    resolver.register_authority("local_admin", "admin")
    resolver.register_authority("backup_admin", "admin")

    execute_proposal({"name": "a", "authority_id": "local_admin", "execute": lambda: {"ok": True}})
    execute_proposal({"name": "b", "authority_id": "backup_admin", "execute": lambda: {"ok": True}})

    state = reconstruct_state("receipts")
    print(state)

    assert state["total_executions"] == 2

if __name__ == "__main__":
    main()