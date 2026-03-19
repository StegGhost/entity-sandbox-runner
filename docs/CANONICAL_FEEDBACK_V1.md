# Canonical Feedback Bundle v1

This bundle adds a feedback layer that reads canonical compaction outputs and converts them into reusable structured feedback.

## Installed
- `install/canonical_feedback.py`
- `config/canonical_feedback_rules.json`
- `docs/CANONICAL_FEEDBACK_V1.md`

## Inputs expected
- `docs/canonical/claims_canonical.md`
- `docs/canonical/definitions_canonical.md`
- `docs/canonical/findings_canonical.md`
- `docs/canonical/compaction_summary.json`
- `docs/canonical/system_summary.md`

## Outputs on run
- `payload/feedback/canonical_feedback.json`
- `payload/feedback/canonical_feedback.md`

## Receipt on run
- `payload/receipts/canonical_feedback/canonical_feedback_0001.json`

## Purpose
Turn compressed canonical knowledge into:
- priority items
- invariant candidates
- contradiction flags
- recommended next actions

## Run
```bash
python install/canonical_feedback.py
```
