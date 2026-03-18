Continuous mode should remain the default append-only ledger.

This bundle adds:
- install/auth_scope.py
- install/lifecycle_manager.py
- config/auth_policy.json

Model:
- StegVerse nodes maintain continuous receipts and integrity records.
- Experiments are user-scoped session records layered on top of the continuous ledger.
- Replays are also user-scoped and stricter than experiments.

Suggested usage:
- start_experiment(owner_id, experiment_name)
- end_experiment(owner_id_hash, experiment_id, result_summary)
- start_replay(owner_id, source_experiment_id)
- end_replay(owner_id_hash, replay_id, summary)
