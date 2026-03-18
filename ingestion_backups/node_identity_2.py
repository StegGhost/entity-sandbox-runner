
import hashlib, os

ID_FILE = "config/node_id.txt"

def get_node_id():
    if os.path.exists(ID_FILE):
        return open(ID_FILE).read().strip()
    nid = hashlib.sha256(os.urandom(32)).hexdigest()
    open(ID_FILE,"w").write(nid)
    return nid
