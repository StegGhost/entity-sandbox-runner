iPhone no-CLI workflow bundle

Purpose:
- updates the Ingestion Pipeline so README/doc bundles are promoted automatically
- no manual python command needed
- after ingestion, the workflow runs install/repo_root_promoter.py
- then commits and pushes the promoted README.md

Install:
- place .github/workflows/ingestion_pipeline.yml into .github/workflows/
- replace the current ingestion workflow with this file

Expected result:
- docs bundle installs to payload/repo_root/
- promoter copies approved files into repo root
- README.md updates automatically
