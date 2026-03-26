"""
SAFE FORCE IMPORT OVERRIDE (FINAL)

- Does NOT override Python's core import system
- Only ensures repo root is importable
- Adds explicit module redirection for known conflicts
- Prevents global interpreter corruption
"""

import sys
import os
import importlib


def activate():
    """
    Safe activation:
    - Ensure repo root is in sys.path
    - Do NOT override __import__
    - Do NOT touch builtins
    """

    repo_root = os.getcwd()

    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    # Ensure install package resolves correctly
    install_path = os.path.join(repo_root, "install")
    if install_path not in sys.path:
        sys.path.insert(0, install_path)

    print("[SAFE IMPORT] sys.path configured")


def force_import(module_name: str):
    """
    Explicit controlled import (used ONLY when needed)
    """
    try:
        return importlib.import_module(module_name)
    except Exception as e:
        print(f"[SAFE IMPORT ERROR] {module_name}: {e}")
        raise
