import os
import shutil


def gossip_receipts(source: str, target: str):
    os.makedirs(target, exist_ok=True)

    for file in os.listdir(source):
        if file.endswith(".json"):
            src = os.path.join(source, file)
            dst = os.path.join(target, file)

            if not os.path.exists(dst):
                shutil.copy2(src, dst)

    return {"status": "gossip_complete"}
