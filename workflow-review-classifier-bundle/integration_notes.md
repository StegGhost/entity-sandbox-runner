# Suggested integration step

Add this directly after workflow files are staged into `workflow_review/`:

```bash
python ingestion/compare_workflows.py
```

## Recommended placement in the safe ingestion workflow

After:

```bash
python ingestion/ingest_bundle_safe.py "$BUNDLE"
```

Add:

```bash
python ingestion/compare_workflows.py
```

## Result

Staged workflow files will not just sit in `workflow_review/`. They will be classified into:

- `workflow_replace/`
- `workflow_deprecated/`

and each one gets a markdown diff report.
