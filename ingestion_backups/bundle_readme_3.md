Sandbox Research Upgrades 106-115

Adds the following auto-ingest research modules:

106. rg_flow_solver.py
107. bootstrap_validation_engine.py
108. symbolic_regression_search.py
109. stability_manifold_explorer.py
110. federated_node_auth_registry.py
111. signed_bundle_verifier.py
112. control_law_synthesizer.py
113. adaptive_intervention_planner.py
114. universality_class_comparator.py
115. discovery_novelty_engine.py

Installation model:
- Files are copied from payload/ into the repo root by install/install_bundle_autoregister.py
- Install receipts are written to evidence_plane/install_receipts/
- Modules use observatory.pipeline_contract decorators so the existing discovery / registry flow can pick them up
