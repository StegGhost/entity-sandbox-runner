# Simple Admissibility Experiment

This is a minimal experiment designed to test the GCAT admissibility bound in isolation. The goal is to verify that the artefact pressure `a` remains within the admissible region defined by:

```
a_{n+1} ≤ K * g_{n+1}^{α} * c_{n+1}^{β} * t_{n+1}^{γ}
```

The experiment uses a very simple transition operator:

- Governance `g` and trust `t` degrade slightly each step (`-0.05` and `-0.03` respectively).
- Constraints `c` remain constant.
- Artefact pressure `a` increases by a fixed `delta_a` proposal.

If the new artefact pressure violates the admissibility inequality, the proposal is rejected and the state does not update. Each state transition (proposal, evaluation and resulting state) is recorded in a receipt chain for auditability.

## Files

- `config.yaml` – parameters for the experiment (initial state, constants, number of steps, and delta_a).
- `run.py` – script to execute the experiment and generate `receipts.json`.
- `receipts.json` – output file containing the list of receipt records (not tracked in version control by default).

## Running

Ensure you have Python 3 and `PyYAML` installed. Then run:

```sh
python run.py
```

The script will read `config.yaml`, perform the simulation, write a chain of receipts into `receipts.json` and print a summary of admissible vs. rejected transitions.
