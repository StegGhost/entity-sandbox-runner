import json
import urllib.request

def fetch_remote_policy(url):
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None
