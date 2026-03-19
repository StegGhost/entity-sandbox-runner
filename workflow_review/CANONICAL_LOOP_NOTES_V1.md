# Canonical Feedback Runner Bundle v1

This bundle adds:
- `install/run_canonical_loop.py`
- `config/canonical_loop_config.json`
- `workflow_review/CANONICAL_LOOP_WORKFLOW_V1.yml.txt`
- `workflow_review/CANONICAL_LOOP_NOTES_V1.md`

Purpose:
- run document compaction
- run canonical feedback
- write a loop report
- provide a ready-to-copy GitHub workflow

Run locally:
```bash
python install/run_canonical_loop.py
```

Staged workflow:
- copy `workflow_review/CANONICAL_LOOP_WORKFLOW_V1.yml.txt`
- paste to `.github/workflows/canonical_loop.yml`
