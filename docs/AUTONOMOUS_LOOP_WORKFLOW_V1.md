# Autonomous Loop Workflow Bundle v1

This installs a GitHub Actions workflow to run the autonomous loop.

Triggers:
- Manual (workflow_dispatch)
- Scheduled (every 6 hours)

What it does:
- Runs autonomous_loop_orchestrator.py
- Commits updated payload outputs

Location after install:
.github/workflows/autonomous_loop.yml
