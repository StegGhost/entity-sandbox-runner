# Workflow Review Classifier Bundle

This bundle upgrades the workflow quarantine system so staged workflow files are automatically compared against
the live `.github/workflows/` versions and then classified.

## What it adds

- `ingestion/compare_workflows.py`
- `workflow_replace/.gitkeep`
- `workflow_deprecated/.gitkeep`

## What it does

After workflow files are staged into `workflow_review/`, the comparison tool:

1. compares each reviewed workflow against `.github/workflows/<same name>`
2. writes a diff report beside the classified result
3. moves the reviewed workflow into one of:

```text
workflow_replace/
workflow_deprecated/
```

## Classification rules

- If no current workflow exists with the same filename → `workflow_replace/`
- If current workflow exists and reviewed file is newer or different → `workflow_replace/`
- If current workflow exists and reviewed file is older or identical → `workflow_deprecated/`

## Report output

For each reviewed workflow, the tool writes:

```text
<filename>.diff.md
```

into the same destination directory.

## Run

```sh
python ingestion/compare_workflows.py
```

## Recommended integration point

Run this immediately after safe ingestion stages files into `workflow_review/`.
