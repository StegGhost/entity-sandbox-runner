# Upload Instructions

1. Create or open the `entity-sandbox-runner` GitHub repo.
2. Upload the contents of this bundle into the repository root.
3. Commit everything together.
4. Run the smoke test workflow or execute locally:

```sh
python -m pip install -r requirements.txt
python runner/orchestrator.py --experiment experiments/admissibility/simple_test
python runner/build_all_artifacts.py --experiment simple_test
python run_visualizations.py
```

## Expected outputs

```text
results/simple_test_results.json
manifests/simple_test_handoff.json
receipts/runs/simple_test_receipts.jsonl
receipts/chains/simple_test_chain.json
reports/latest/simple_test_summary.md
reports/validation/admissibility_validation_summary.json
data_records/canonical/admissibility_observations.jsonl
data_records/aggregates/admissibility_stats.json
```
