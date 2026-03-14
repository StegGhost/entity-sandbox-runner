import json
from pathlib import Path
from datetime import datetime

REGISTRY = Path("module_registry.json")

def load_registry():

    if not REGISTRY.exists():
        return {}

    return json.loads(REGISTRY.read_text())

def save_registry(data):

    REGISTRY.write_text(json.dumps(data, indent=2))


def record_install(bundle_name, version):

    reg = load_registry()

    reg[bundle_name] = {
        "version": version,
        "installed": datetime.utcnow().isoformat()
    }

    save_registry(reg)
