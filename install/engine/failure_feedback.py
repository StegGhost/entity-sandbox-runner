from pathlib import Path


def load_failure_text(path="logs/latest_failure.txt"):
    p = Path(path)
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def save_failure_text(text: str, path="logs/latest_failure.txt"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return str(p)
