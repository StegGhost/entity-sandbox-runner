# V6.5 No-CLI Automation Bundle

## Purpose
This bundle removes the need to run Python manually from iPhone.

## What it adds
- `payload/workflows/promote_staged_workflows.yml`
- `payload/workflows/run_evaluation.yml`
- `install/unified_promotion_patch.py`

## Flow after install
1. Ingestion installs the bundle.
2. Existing promotion path stages the workflow files in `payload/workflows/`.
3. The **Promote Staged Workflows** GitHub Action copies staged workflows into `.github/workflows/`.
4. The **Run Evaluation** GitHub Action runs automatically when evaluation files change, or manually via Actions UI.

## iPhone-native usage
You should not need shell access.
After this is installed and promoted, use the GitHub Actions UI:
- trigger **Promote Staged Workflows** if needed
- then trigger **Run Evaluation** or let it run on push

## Expected visible outcome
Actions tab should eventually show:
- `Promote Staged Workflows`
- `Run Evaluation`
