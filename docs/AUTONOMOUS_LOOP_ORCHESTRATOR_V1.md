# Autonomous Loop Orchestrator Bundle v1

This bundle runs the FULL governed loop automatically.

Sequence:
1. document_compactor
2. canonical_feedback
3. knowledge_delta
4. canonical_receipt_binder
5. feedback_injection
6. feedback_execution_bridge

Outputs:
- payload/runtime/autonomous_loop_report.json

Run:
python install/autonomous_loop_orchestrator.py

Purpose:
- eliminate manual sequencing
- ensure deterministic loop execution
- provide single-run system evolution
