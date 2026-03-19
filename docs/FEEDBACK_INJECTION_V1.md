# Feedback Injection Bundle v1

This bundle injects canonical feedback into reusable prompt and policy input files.

Installed:
- `install/feedback_injection.py`
- `config/feedback_injection_config.json`
- `docs/FEEDBACK_INJECTION_V1.md`

Expected input:
- `payload/feedback/canonical_feedback.json`

Outputs on run:
- `payload/injection/feedback_prompt_inputs.json`
- `payload/injection/feedback_prompt_inputs.md`
- `payload/injection/feedback_policy_inputs.json`
- `payload/receipts/feedback_injection/feedback_injection_0001.json`

Run:
```bash
python install/feedback_injection.py
```
