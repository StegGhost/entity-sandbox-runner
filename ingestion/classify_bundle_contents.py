from pathlib import Path

def classify_files(extracted_root: Path):
    normal_files = []
    workflow_files = []

    for item in extracted_root.rglob("*"):
        if item.is_dir():
            continue

        rel = item.relative_to(extracted_root)
        rel_str = str(rel).replace("\\", "/")

        if "/.github/workflows/" in f"/{rel_str}" or rel_str.startswith(".github/workflows/"):
            workflow_files.append(rel)
        else:
            normal_files.append(rel)

    return normal_files, workflow_files
