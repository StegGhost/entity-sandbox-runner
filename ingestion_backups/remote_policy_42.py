
import json, urllib.request

def fetch_remote_policy(url):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return json.loads(r.read().decode())
    except:
        return None
