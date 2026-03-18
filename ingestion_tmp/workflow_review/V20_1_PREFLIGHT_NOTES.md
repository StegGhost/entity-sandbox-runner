Autonomous v20.1 preflight bundle

Purpose:
- verify repo state against a canonical hash for the selected run type
- compare live repo files to canonical files
- auto-heal changed or missing files from canonical source
- ensure workflow files are also part of preflight coverage
- record preflight receipt into payload/integrity before the experiment run

Install target:
- entity-sandbox-runner

Workflow:
- replace your current workflow with .github/workflows/forced_ingest_and_eval.yml
- optionally run with workflow_dispatch input run_type=adaptive_v20

Important:
- this bundle uses full-file canonical replacements for critical files
- canonical files live under payload/canonical_repo/
