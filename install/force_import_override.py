"""
SAFE FORCE IMPORT OVERRIDE (FINAL)

- Only overrides specific modules (receipt_chain)
- Does NOT hijack global import system
- Prevents breaking internal package imports
"""

import sys
import os
import importlib.util


def _force_module(module_name: str, file_path: str):
    if not os.path.exists(file_path):
        return False

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sys.modules[module_name] = module
    return True


def activate():
    root = os.getcwd()

    candidates = [
        os.path.join(root, "receipt_chain.py"),
        os.path.join(root, "engine", "receipt_chain.py"),
        os.path.join(root, "install", "engine", "receipt_chain.py"),
    ]

    for path in candidates:
        if _force_module("receipt_chain", path):
            print(f"[SAFE IMPORT OVERRIDE] receipt_chain -> {path}")
            break
