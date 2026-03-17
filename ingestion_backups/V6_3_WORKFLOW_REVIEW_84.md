# V6.3 Workflow Bundle — Automated Evaluation

This bundle stages an automated GitHub Actions workflow for evaluation.

## Included
- `payload/workflows/run_evaluation.yml`
- `install/promote_workflow.py`

## Why staged instead of direct
Your ingestion boundary treats workflow material specially. This bundle keeps the workflow in a safe staged location so it can be reviewed and then promoted into:

- `.github/workflows/run_evaluation.yml`

## What the workflow does
- Triggers on pushes touching:
  - `install/**`
  - `experiments/**`
  - `payload/**`
- Supports manual trigger via `workflow_dispatch`
- Runs:
  - `python experiments/evaluation_suite/run_eval.py`

## Promotion step
After review, run:

```bash
python install/promote_workflow.py
```

Then commit the promoted workflow file.
