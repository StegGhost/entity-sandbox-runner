# Knowledge Delta Bundle v1

This bundle adds deterministic tracking of changes between canonical knowledge states.

Installed:
- `install/knowledge_delta.py`
- `config/knowledge_delta_config.json`
- `docs/KNOWLEDGE_DELTA_V1.md`

Expected inputs:
- `docs/canonical/claims_canonical.md`
- `docs/canonical/definitions_canonical.md`
- `docs/canonical/findings_canonical.md`
- `docs/canonical/compaction_summary.json`

Outputs:
- `payload/knowledge_delta/knowledge_delta.json`
- `payload/knowledge_delta/knowledge_delta.md`
- `payload/receipts/knowledge_delta/knowledge_delta_0001.json`
- `docs/canonical/index.json`

Run:
```bash
python install/knowledge_delta.py
```
