v14.3–v15 bundle

What it adds:
- signed remote policy acceptance
- rejection logging for malformed/untrusted remote policy
- Fin-Co signal injection
- local control-plane override hook
- early multi-node / cross-node consensus signal

Files to apply:
- experiments/evaluation_suite/run_eval.py
- install/policy_engine.py
- install/policy_signature.py
- install/remote_policy.py
- install/node_consensus.py
- install/control_plane.py
- install/finco.py
- config/policy.json
- payload/control_plane/override.json
- .github/workflows/autonomous_v15.yml

iPhone note:
- workflow is placed in github_workflows/autonomous_v15.yml so it remains visible in Files
- move it to .github/workflows/autonomous_v15.yml in the repo
