
import json, urllib.request

def fetch_peer(url):
    try:
        return json.loads(urllib.request.urlopen(url,timeout=2).read().decode())
    except:
        return None
