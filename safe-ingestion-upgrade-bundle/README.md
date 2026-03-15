# Safe Ingestion Upgrade Bundle

This bundle upgrades the ingestion system to support:

- manifest-driven verification
- workflow-file segregation
- installed / failed / archived bundle movement
- confirmation report generation
- manual review staging for `.github/workflows/*`

## What this solves

GitHub blocks the workflow from auto-committing workflow-file changes in the same way as normal files.
This upgrade separates those privileged files from normal file installs so ingestion can still succeed and be verified.

## New lifecycle

```text
incoming_bundles/
    my_bundle.zip
        ↓
ingestion
        ↓
verify expected files
        ↓
normal files committed
workflow files staged in workflow_review/
        ↓
bundle moved to:
    installed_bundles/
or failed_bundles/
```

## Included files

```text
ingestion/
    ingest_bundle_safe.py
    verify_installation.py
    classify_bundle_contents.py
    move_processed_bundle.py
    write_install_report.py
    find_all_bundles.py

.github/workflows/
    safe-ingest-all-bundles.yml

workflow_review/
    .gitkeep

installed_bundles/
    .gitkeep

failed_bundles/
    .gitkeep
```

## Key behavior

- normal files are installed into the repo
- `.github/workflows/*` files are copied into `workflow_review/`
- manifest expectations are checked after install
- a JSON confirmation report is written into `ingestion_reports/`
- bundle is moved to `installed_bundles/` or `failed_bundles/`
