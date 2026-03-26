import sys
import os
import importlib.util


def _load_and_force(module_name, path):
    if not os.path.exists(path):
        return False

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sys.modules[module_name] = module
    return True


def pytest_configure(config):
    root = os.getcwd()

    candidates = [
        os.path.join(root, "receipt_chain.py"),
        os.path.join(root, "engine", "receipt_chain.py"),
        os.path.join(root, "install", "engine", "receipt_chain.py"),
    ]

    loaded = False
    for path in candidates:
        if _load_and_force("receipt_chain", path):
            print(f"[FORCE IMPORT] receipt_chain -> {path}")
            loaded = True
            break

    if not loaded:
        print("[FORCE IMPORT] receipt_chain NOT FOUND")
