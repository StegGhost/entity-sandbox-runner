name: Run Brain

on:
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run brain
        id: run_brain
        continue-on-error: true
        run: python internal_brain/brain_runner.py

      - name: Show brain report
        if: always()
        run: cat internal_brain/brain_report.json

      - name: Fail workflow if brain failed
        if: steps.run_brain.outcome != 'success'
        run: exit 1
