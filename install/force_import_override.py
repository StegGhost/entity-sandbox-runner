import importlib
import sys
import os
from types import ModuleType
from pathlib import Path
import time


# 🔥 CONFIG: modules you want to control
FORCED_MODULES = {
    "receipt_chain": [
        "engine/receipt_chain.py",
        "receipt_chain.py",
        "install/engine/receipt_chain.py",
    ],
    "replay_engine": [
        "engine/replay_engine.py",
        "replay_engine.py",
        "install/engine/replay_engine.py",
    ]
}


TRACE_FILE = "brain_reports/import_override_trace.jsonl"


def log_trace(event: dict):
    os.makedirs("brain_reports", exist_ok=True)
    with open(TRACE_FILE, "a") as f:
        f.write(f"{event}\n")


def resolve_first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def load_module_from_path(module_name: str, file_path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def force_import(module_name: str):

    if module_name not in FORCED_MODULES:
        return None

    candidate_paths = FORCED_MODULES[module_name]
    selected = resolve_first_existing(candidate_paths)

    if not selected:
        log_trace({
            "ts": time.time(),
            "module": module_name,
            "status": "not_found",
            "candidates": candidate_paths
        })
        return None

    module = load_module_from_path(module_name, selected)

    sys.modules[module_name] = module

    log_trace({
        "ts": time.time(),
        "module": module_name,
        "status": "forced",
        "path": selected
    })

    return module


# 🔥 GLOBAL HOOK
_original_import = __import__


def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name in FORCED_MODULES:
        module = force_import(name)
        if module:
            return module

    return _original_import(name, globals, locals, fromlist, level)


def activate():
    sys.meta_path = []  # 🔥 kill meta importers (optional hard mode)
    builtins = __import__.__globals__
    builtins["__import__"] = custom_import

    log_trace({
        "ts": time.time(),
        "event": "force_import_override_activated"
    })
