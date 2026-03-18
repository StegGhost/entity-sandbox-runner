JSON-safe fix bundle

Purpose:
- Prevent crashes caused by .gitkeep or empty files inside payload/receipts and payload/replay
- Ignore any non-.json files during chain verification and replay loading
- Keep current BCAT v12 flow intact

Files included:
- install/safe_json.py
- install/crypto_keys.py
- install/replay.py
- experiments/evaluation_suite/run_eval.py
- github_workflows/autonomous_v12.yml

Important:
- Move github_workflows/autonomous_v12.yml to .github/workflows/autonomous_v12.yml in the repo.
- This fix is specifically for payload/receipts/.gitkeep and payload/replay/.gitkeep cases.
