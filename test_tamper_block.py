import os, json, shutil
from governed_executor import execute_proposal, resolver
from receipt_chain_verifier import clear_chain_lock

def main():
    clear_chain_lock()
    shutil.rmtree("receipts", ignore_errors=True)
    os.makedirs("receipts", exist_ok=True)

    resolver.register_authority("local_admin", "admin")

    p = {"name": "test", "authority_id": "local_admin", "execute": lambda: {"ok": True}}

    r1 = execute_proposal(p)
    print("FIRST:", r1)

    files = os.listdir("receipts")
    path = os.path.join("receipts", files[0])

    data = json.load(open(path))
    data["tampered"] = True
    json.dump(data, open(path, "w"), indent=2)

    r2 = execute_proposal(p)
    print("SECOND:", r2)

    assert r2["status"] == "rejected"

if __name__ == "__main__":
    main()