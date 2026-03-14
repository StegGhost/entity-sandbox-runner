# Entity Sandbox Runner

Entity Sandbox Runner is StegVerse's experimental sandbox foundation for GCAT / BCAT experiments.

It is structured so experiment execution, provenance, human-readable reports, and canonical machine-usable records remain clearly separated.

## Data lifecycle

### `results/`
Run-local raw outputs. Useful for immediate inspection and reproducibility, but not the canonical long-term evidence layer.

### `receipts/`
The provenance reference layer. Receipts should indicate:
- what happened
- what data was captured
- where it was stored
- which downstream artifacts used it

### `reports/`
Human-readable artifacts derived from results and receipts.

### `data_records/`
Canonical machine-usable evidence accumulated across experiments.

### `manifests/`
Portable metadata for downstream ingest, export, and SDK packaging.

## Repository structure

```text
entity-sandbox-runner/
├─ experiments/
├─ runner/
├─ sandbox/
├─ observatory/
├─ interaction_graph/
├─ adaptive_scanner/
├─ statistics/
├─ reproducibility/
├─ visualization/
├─ sdk/
├─ entities/
├─ results/
├─ receipts/
├─ reports/
├─ data_records/
└─ manifests/
```

## How data is derived, compiled, utilized, saved, and kept

1. a scenario config is loaded from `experiments/.../config.yaml`
2. the runner executes the scenario and writes local results into `results/`
3. receipts are written into `receipts/`
4. canonical observations are appended into `data_records/canonical/`
5. aggregates are recomputed into `data_records/aggregates/`
6. readable reports are written into `reports/`
7. manifests are written into `manifests/`

Canonical records should be appended and preserved. Aggregate files should be rebuilt from canonical records whenever possible.

## Quick start

```sh
python -m pip install -r requirements.txt
python runner/orchestrator.py --experiment experiments/admissibility/simple_test
python runner/build_all_artifacts.py --experiment simple_test
python run_visualizations.py
python run_repro_bundle.py --results results/simple_test_results.json
```
