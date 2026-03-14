# Entity Sandbox Runner

# Entity Sandbox Runner

Entity Sandbox Runner is a scenario orchestration environment for testing
GCAT / BCAT sandbox entities under controlled experimental conditions.

The system executes isolated and multi‑entity scenarios, records local receipts,
and prepares normalized outputs for downstream governance evaluation by the
StegVerse ingest runtime.

This repository is a **scenario generator and sandbox simulator**.
Outputs are intended to be evaluated by the **demo_ingest_engine** governance runtime.

Pipeline:

entity-sandbox-runner
      ↓
proposal manifest
      ↓
demo_ingest_engine
      ↓
governance evaluation
      ↓
verification + replay

## Running

Example:

python runner/orchestrator.py --experiment experiments/admissibility/simple_test

Outputs:

results/simple_test_results.json
manifests/simple_test_handoff.json

This repository orchestrates the execution of StegVerse GCAT/BCAT sandbox experiments in a standalone environment.  It contains everything needed to run a single experiment, capture its output, and store results for later analysis.  The initial release includes the *simple admissibility test* from the `entity‑sandbox` project.

## Purpose

- **Automation** – run sandbox experiments without a graphical environment, using a GitHub workflow or local shell.
- **Observability** – generate human‑readable summaries and audit trails of each experiment run.
- **Isolation** – keep experimental code and outputs separate from production systems and secret tokens.

## Structure

- `run.py` – Python script implementing the simple admissibility experiment.  Reads `config.yaml`, simulates state transitions, enforces the GCAT admissibility inequality and prints a summary.
- `config.yaml` – configuration for the experiment (initial state, constants, step count and artefact increment).
- `.gitignore` – ignores generated receipts and local Python caches.
- `.github/workflows/run-simple-test.yml` – GitHub Actions workflow that runs the experiment and uploads its output.
- `results/example_results.txt` – sample results from a completed run.

You can extend this runner by adding additional experiment scripts under subfolders and updating the workflow accordingly.

## Running Locally

Install Python 3 and PyYAML:

```sh
python -m pip install pyyaml
```

Then run:

```sh
python run.py > results/example_results.txt
```

This reads `config.yaml`, runs the experiment and writes a summary.  It also writes a chain of receipts into `receipts.json` (ignored by version control).

## Automated Execution

The included workflow (`.github/workflows/run-simple-test.yml`) defines a job that checks out the repository, installs Python and PyYAML, runs `python run.py`, writes a results file in the `results` directory and uploads it as an artifact.  You can trigger the workflow from the GitHub Actions tab or schedule it to run periodically by adding a `schedule` trigger.

# Experiment

This folder defines a sandbox experiment scenario.

Each experiment includes:

- configuration parameters
- transition rules
- expected admissibility behavior

The orchestrator loads the configuration and executes the
scenario step‑by‑step while recording a receipt chain.

Outputs are written to:

results/
manifests/
