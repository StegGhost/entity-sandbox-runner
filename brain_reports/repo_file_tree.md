# Repo File Tree

Generated: 2026-03-25T03:30:13.349980+00:00

```text
entity-sandbox-runner/
├── .github
│   └── workflows
│       ├── actuator_bridge.yml
│       ├── anomaly_detection_workflow.yml
│       ├── autonomous.yml
│       ├── autonomous_loop.yml
│       ├── bootstrap_promoter.yml
│       ├── brain-sync.yml
│       ├── bundle-orchestrator.yml
│       ├── decision_engine.yml
│       ├── document_engine.yml
│       ├── execution_policy_engine.yml
│       ├── forced_ingest_and_eval.yml
│       ├── goal_directed_execution.yml
│       ├── governed_system_master.yml
│       ├── governed_system_master_modes.yml
│       ├── ingestion.yml
│       ├── llm_adapter_validation.yml
│       ├── observatory-smoke.yml
│       ├── pattern_memory.yml
│       ├── promote-platform.yml
│       ├── promote-runtime-ledger.yml
│       ├── promote_staged_workflows.yml
│       ├── repo-map.yml
│       ├── run-brain.yml
│       ├── run_evaluation.yml
│       ├── run_experiment.yml
│       ├── sandbox-runner.yml
│       ├── sandbox-smoke-test.yml
│       ├── sandbox-visualize.yml
│       ├── self_improve_loop.yml
│       ├── snapshot_workflow.yml
│       ├── state_scoring_workflow.yml
│       ├── test_and_feedback.yml
│       └── validate_governed_executor.yml
├── _ingest_tmp
│   ├── autonomous_v20_1_preflight_bundle.zip
│   │   ├── .github
│   │   │   └── workflows
│   │   │       └── forced_ingest_and_eval.yml
│   │   ├── config
│   │   │   ├── experiment_profiles.json
│   │   │   └── policy.json
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── install
│   │   │   ├── bcat_engine.py
│   │   │   ├── consensus_engine.py
│   │   │   ├── crypto_keys.py
│   │   │   ├── network_registry.py
│   │   │   ├── policy_engine.py
│   │   │   ├── preflight_canonical.py
│   │   │   └── receipt_guard.py
│   │   ├── payload
│   │   │   └── canonical_repo
│   │   │       ├── .github
│   │   │       │   └── workflows
│   │   │       │       └── forced_ingest_and_eval.yml
│   │   │       ├── config
│   │   │       │   └── policy.json
│   │   │       ├── experiments
│   │   │       │   └── evaluation_suite
│   │   │       │       └── run_eval.py
│   │   │       └── install
│   │   │           ├── bcat_engine.py
│   │   │           ├── consensus_engine.py
│   │   │           ├── crypto_keys.py
│   │   │           ├── network_registry.py
│   │   │           ├── policy_engine.py
│   │   │           └── receipt_guard.py
│   │   ├── workflow_review
│   │   │   └── V20_1_PREFLIGHT_NOTES.md
│   │   └── bundle_manifest.json
│   ├── dsr_bundle_v2.zip
│   │   ├── payload
│   │   │   ├── decision_state_recorder.py
│   │   │   ├── example.py
│   │   │   ├── receipt_chain.py
│   │   │   └── stability_governor.py
│   │   └── bundle_manifest.json
│   ├── entity_sandbox_runner_lifecycle_auth_bundle.zip
│   │   ├── config
│   │   │   └── auth_policy.json
│   │   ├── install
│   │   │   ├── auth_scope.py
│   │   │   └── lifecycle_manager.py
│   │   ├── workflow_review
│   │   │   └── LIFECYCLE_AUTH_NOTES.md
│   │   └── bundle_manifest.json
│   ├── sandbox_eval_ready_bundle.zip
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── install
│   │   │   ├── eval_metrics.py
│   │   │   ├── eval_orchestrator.py
│   │   │   └── stability_governor.py
│   │   ├── payload
│   │   │   └── config
│   │   │       └── eval_config.json
│   │   └── workflow_review
│   │       └── EVAL_NOTES.md
│   ├── sandbox_eval_wiring_patch_v6_1.zip
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── install
│   │   │   ├── eval_metrics.py
│   │   │   ├── eval_orchestrator.py
│   │   │   └── stability_governor.py
│   │   ├── payload
│   │   │   └── config
│   │   │       └── eval_config.json
│   │   └── workflow_review
│   │       └── EVAL_WIRING_PATCH.md
│   ├── sandbox_v11_1_to_12_bundle.zip
│   │   ├── config
│   │   │   └── policy.json
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── github_workflows
│   │   │   └── autonomous_v12.yml
│   │   ├── install
│   │   │   ├── bcat_engine.py
│   │   │   ├── crypto_keys.py
│   │   │   ├── policy_engine.py
│   │   │   └── replay.py
│   │   └── README.md
│   ├── sandbox_v14_3_to_v15_bundle.zip
│   │   ├── config
│   │   │   └── policy.json
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── github_workflows
│   │   │   └── autonomous_v15.yml
│   │   ├── install
│   │   │   ├── control_plane.py
│   │   │   ├── finco.py
│   │   │   ├── node_consensus.py
│   │   │   ├── policy_engine.py
│   │   │   ├── policy_signature.py
│   │   │   └── remote_policy.py
│   │   ├── payload
│   │   │   └── control_plane
│   │   │       └── override.json
│   │   └── workflow_review
│   │       └── V14_3_TO_V15_NOTES.md
│   ├── sandbox_v6_2_shared_state_patch.zip
│   │   ├── install
│   │   │   ├── adaptive_scheduler.py
│   │   │   ├── eval_metrics.py
│   │   │   ├── eval_orchestrator.py
│   │   │   └── system_state.py
│   │   └── workflow_review
│   │       └── V6_2_SHARED_STATE_PATCH.md
│   ├── sandbox_v6_3_workflow_bundle.zip
│   │   ├── install
│   │   │   └── promote_workflow.py
│   │   ├── payload
│   │   │   └── workflows
│   │   │       └── run_evaluation.yml
│   │   └── workflow_review
│   │       ├── BUILD_NOTES.md
│   │       └── V6_3_WORKFLOW_REVIEW.md
│   ├── sandbox_v6_4_unified_promotion_bundle.zip
│   │   ├── install
│   │   │   ├── bundle_manifest.json
│   │   │   └── unified_promotion_patch.py
│   │   └── workflow_review
│   │       └── V6_4_REVIEW.md
│   ├── sandbox_v6_5_no_cli_automation_bundle.zip
│   │   ├── install
│   │   │   └── unified_promotion_patch.py
│   │   ├── payload
│   │   │   └── workflows
│   │   │       ├── promote_staged_workflows.yml
│   │   │       └── run_evaluation.yml
│   │   └── workflow_review
│   │       ├── BUILD_NOTES.md
│   │       └── V6_5_NO_CLI_AUTOMATION.md
│   ├── sandbox_v7_1_stabilization_bundle.zip
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── install
│   │   │   └── stability_governor.py
│   │   └── README.md
│   ├── sandbox_v7_2_autonomous_persistence_bundle.zip
│   │   ├── .github
│   │   │   └── workflows
│   │   │       └── autonomous_loop.yml
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   └── README.md
│   ├── sandbox_v7_6_to_7_9_bundle.zip
│   │   ├── .github
│   │   │   └── workflows
│   │   │       └── autonomous_loop.yml
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   └── README.md
│   ├── sandbox_v7_autonomous_loop_bundle.zip
│   │   ├── experiments
│   │   │   └── autonomous
│   │   │       └── autonomous_controller.py
│   │   ├── install
│   │   │   ├── bundle_manifest.json
│   │   │   └── orchestrator_hook.py
│   │   ├── payload
│   │   │   └── loop_state.json
│   │   └── workflow_review
│   │       └── V7_README.md
│   ├── sandbox_v8_1_to_8_5_bundle.zip
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── github_workflows
│   │   │   └── autonomous_loop.yml
│   │   ├── install
│   │   │   ├── coordination.py
│   │   │   ├── deterministic_enforcer.py
│   │   │   ├── economic_weighting.py
│   │   │   ├── external_signal_adapter.py
│   │   │   └── receipt_logger.py
│   │   └── README.md
│   ├── sandbox_v8_governed_system_bundle.zip
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── github_workflows
│   │   │   └── autonomous_loop.yml
│   │   ├── install
│   │   │   ├── coordination.py
│   │   │   ├── deterministic_enforcer.py
│   │   │   ├── economic_weighting.py
│   │   │   ├── external_signal_adapter.py
│   │   │   └── receipt_logger.py
│   │   ├── payload
│   │   │   └── config
│   │   │       └── v8_policy.json
│   │   ├── workflow_review
│   │   │   └── V8_NOTES.md
│   │   └── README.md
│   ├── sandbox_v9_1_to_10_bundle.zip
│   │   ├── config
│   │   │   └── policy.json
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── github_workflows
│   │   │   └── autonomous_v10.yml
│   │   ├── install
│   │   │   ├── crypto.py
│   │   │   ├── policy_engine.py
│   │   │   └── replay.py
│   │   └── README.md
│   ├── stegverse_docs_bundle.zip
│   │   ├── payload
│   │   │   ├── architecture_map.md
│   │   │   ├── diagram.md
│   │   │   └── README.md
│   │   └── bundle_manifest.json
│   ├── stegverse_docs_v2_bundle.zip
│   │   ├── payload
│   │   │   ├── Architecture_Diagram_v2.pdf
│   │   │   ├── architecture_map.md
│   │   │   ├── README.md
│   │   │   └── StegVerse_Formal_Spec_v2.pdf
│   │   └── bundle_manifest.json
│   ├── v13_1_to_v14_bundle.zip
│   │   ├── .github
│   │   │   └── workflows
│   │   │       └── autonomous_v14.yml
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   └── install
│   │       ├── cross_verify.py
│   │       ├── finco.py
│   │       └── remote_policy.py
│   ├── v21_1_gatekeeper_bundle.zip
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── install
│   │   │   ├── ingestion_v2.py
│   │   │   └── preflight_strict.py
│   │   ├── workflow_review
│   │   │   └── run.yml
│   │   └── bundle_manifest.json
│   ├── v21_strict_system_bundle.zip
│   │   ├── .github
│   │   │   └── workflows
│   │   │       └── run.yml
│   │   ├── config
│   │   │   ├── experiment_profiles.json
│   │   │   └── policy.json
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   ├── install
│   │   │   └── preflight_strict.py
│   │   ├── payload
│   │   │   └── canonical_repo
│   │   │       └── adaptive_v20
│   │   │           ├── .github
│   │   │           │   └── workflows
│   │   │           │       └── run.yml
│   │   │           ├── config
│   │   │           │   └── policy.json
│   │   │           └── experiments
│   │   │               └── evaluation_suite
│   │   │                   └── run_eval.py
│   │   ├── workflow_review
│   │   │   └── V21_NOTES.md
│   │   └── bundle_manifest.json
│   └── v21_to_v30_bundle.zip
│       ├── experiments
│       │   └── evaluation_suite
│       │       └── run_eval.py
│       ├── github_workflows
│       │   └── v30.yml
│       └── install
│           ├── anomaly.py
│           ├── arbitration.py
│           ├── audit.py
│           ├── drift.py
│           ├── node_identity.py
│           ├── peer_verification.py
│           ├── policy_voting.py
│           ├── quorum.py
│           ├── remote_ingest.py
│           └── reputation_decay.py
├── _tmp_bundle_rigel_number
│   ├── payload
│   │   └── repo_root
│   │       └── docs
│   │           └── Rigel Number
│   │               ├── metadata.json
│   │               ├── paper.md
│   │               └── paper.tex
│   └── bundle_manifest.json
├── adaptive_scanner
│   ├── __init__.py
│   ├── boundary_locator.py
│   └── refinement_grid.py
├── autonomy_plane
│   ├── adaptive_boundary_targeter.py
│   ├── adaptive_shard_reweighting_engine.py
│   ├── autonomous_baseline_builder.py
│   ├── autonomous_summary_notary.py
│   ├── autonomy_safety_gate.py
│   ├── boundary_focus_controller.py
│   ├── candidate_law_compactor.py
│   ├── candidate_law_promotion_gate.py
│   ├── convergence_certificate_builder.py
│   ├── convergence_stop_recommender.py
│   ├── counterexample_hunter.py
│   ├── critical_region_queue.py
│   ├── cross_scale_target_allocator.py
│   ├── disagreement_retest_scheduler.py
│   ├── discovery_receipt_writer.py
│   ├── experiment_retry_policy_builder.py
│   ├── experiment_space_pruner.py
│   ├── exploration_reward_model.py
│   ├── followup_run_recommender.py
│   ├── global_boundary_snapshotter.py
│   ├── law_stability_dashboard.py
│   ├── meta_hypothesis_ranker.py
│   ├── phase_transition_scorecard.py
│   ├── regime_shift_alert_engine.py
│   ├── replication_priority_router.py
│   ├── research_checkpoint_writer.py
│   ├── research_goal_router.py
│   ├── result_salience_estimator.py
│   ├── theorem_refinement_loop.py
│   └── uncertainty_gradient_mapper.py
├── brain_reports
│   ├── admissibility_state.json
│   ├── brain_report_latest.json
│   ├── bundle_inventory.json
│   ├── bundle_inventory.md
│   ├── execute_next_action_result.json
│   ├── failed_bundle_report_correlation.json
│   ├── next_action.json
│   ├── receipt_catalog.json
│   ├── receipt_index.jsonl
│   └── receipt_reconciled_state.json
├── bundle_examples
│   └── example_bundle_manifest.json
├── cluster_plane
│   ├── campaign_retry_controller.py
│   ├── cluster_artifact_cache.py
│   ├── cluster_execution_manifest.json
│   ├── compute_budget_allocator.py
│   ├── cross_cluster_merge_coordinator.py
│   ├── distributed_run_manifest_builder.py
│   ├── distributed_seed_namespace.py
│   ├── distributed_shard_scheduler.py
│   ├── result_shard_consolidator.py
│   ├── worker_capacity_registry.py
│   └── worker_failure_recovery_stub.py
├── config
│   ├── actuator_bridge_config.json
│   ├── adaptive_priority_config.json
│   ├── anomaly_detection_config.json
│   ├── anomaly_detection_workflow_config.json
│   ├── auth_policy.json
│   ├── autonomous_loop_config.json
│   ├── canonical_feedback_rules.json
│   ├── canonical_loop_config.json
│   ├── canonical_receipt_binder_config.json
│   ├── distributed_worker_config.json
│   ├── document_compactor_config.json
│   ├── document_engine_config.json
│   ├── execution_policy_engine_config.json
│   ├── experience_policy.json
│   ├── experiment_profiles.json
│   ├── failure_recovery_config.json
│   ├── feedback_execution_bridge_config.json
│   ├── feedback_injection_config.json
│   ├── goal_directed_execution_config.json
│   ├── knowledge_delta_config.json
│   ├── marketing_system_config.json
│   ├── marketing_workflow_config.json
│   ├── pattern_memory_config.json
│   ├── policy.json
│   ├── preflight_guard_config.json
│   ├── publication_engine_config.json
│   ├── repo_integrity_manifest.json
│   ├── repo_root_promoter_rules.json
│   ├── rigel_policy.json
│   ├── rollback_engine_config.json
│   ├── self_modifying_loop_config.json
│   ├── state_scoring_config.json
│   └── state_scoring_workflow_config.json
├── control_plane
│   ├── tc
│   │   ├── bundle_install.tc.json
│   │   └── README.md
│   ├── tvc
│   │   ├── README.md
│   │   └── verify_bundle_install.py
│   ├── .gitkeep
│   ├── override.json
│   ├── README.md
│   └── stability_governor.py
├── data_records
│   └── README.md
├── discovery_engine
│   ├── adaptive_campaign_auditor.py
│   ├── adaptive_information_budgeter.py
│   ├── boundary_shape_classifier.py
│   ├── campaign_auto_stop_detector.py
│   ├── critical_band_navigator.py
│   ├── critical_ratio_competitor_search.py
│   ├── cross_dataset_novelty_monitor.py
│   ├── cross_domain_transfer_planner.py
│   ├── evidence_density_tracker.py
│   ├── experiment_termination_policy.py
│   ├── followup_campaign_generator.py
│   ├── high_value_boundary_sampler.py
│   ├── invariant_retention_scheduler.py
│   ├── novelty_score_estimator.py
│   ├── symbolic_regression_stub.py
│   └── transition_regime_labeler.py
├── docs
│   ├── architecture
│   │   ├── ARCHITECTURE_DIAGRAM.md
│   │   └── PROPOSED_BUILD.md
│   ├── canonical
│   │   ├── claims_canonical.md
│   │   ├── compaction_summary.json
│   │   ├── definitions_canonical.md
│   │   ├── findings_canonical.md
│   │   ├── index.json
│   │   └── system_summary.md
│   ├── demo_suite_suggestions
│   │   └── critical_ratio_campaign
│   │       ├── baselines.py
│   │       ├── CLAIMS.md
│   │       ├── expected_outputs.json
│   │       ├── experiment_config.json
│   │       ├── falsification_tests.py
│   │       ├── protocol.md
│   │       ├── README.md
│   │       └── validate_results.py
│   ├── research
│   │   └── RUNTIME_THEORY.md
│   ├── ACTUATOR_BRIDGE_V1A.md
│   ├── ADAPTIVE_PRIORITY_ENGINE_V1.md
│   ├── ANOMALY_DETECTION_V1.md
│   ├── ANOMALY_DETECTION_WORKFLOW_V1.md
│   ├── AUTONOMOUS_LOOP_ORCHESTRATOR_V1.md
│   ├── AUTONOMOUS_LOOP_WORKFLOW_V1.md
│   ├── CANONICAL_FEEDBACK_V1.md
│   ├── CANONICAL_RECEIPT_BINDER_V1.md
│   ├── CEM_spec.md
│   ├── DISTRIBUTED_WORKER_V1.md
│   ├── DOCUMENT_COMPRESSION_V1A_MINIMAL.md
│   ├── EXECUTION_POLICY_ENGINE_V1A.md
│   ├── FAILURE_RECOVERY_V1.md
│   ├── FEEDBACK_EXECUTION_BRIDGE_V1.md
│   ├── FEEDBACK_INJECTION_V1.md
│   ├── formal_model.md
│   ├── GOAL_DIRECTED_EXECUTION_V1A.md
│   ├── KNOWLEDGE_DELTA_V1.md
│   ├── MARKETING_SYSTEM_V1.md
│   ├── MARKETING_WORKFLOW_V1.md
│   ├── PATTERN_MEMORY_V1A.md
│   ├── PREFLIGHT_GUARD_V1.md
│   ├── README_bundle_notes.md
│   ├── ROLLBACK_ENGINE_V1.md
│   ├── SELF_MODIFYING_LOOP_V1A.md
│   ├── STATE_SCORING_V1.md
│   └── STATE_SCORING_WORKFLOW_V1.md
├── engine
│   ├── failure_feedback.py
│   ├── gap_signals.py
│   ├── llm_self_improve.py
│   ├── priority_router.py
│   ├── proposal_to_bundle.py
│   ├── repo_snapshot.py
│   └── self_improve_runner.py
├── entities
│   ├── sandbox_A.yaml
│   └── sandbox_B.yaml
├── evidence_plane
│   ├── install_receipts
│   │   ├── bundle_install_receipt.json
│   │   └── sandbox_research_upgrades_106_115_v1_install_receipt.json
│   ├── ledger
│   │   ├── append_ledger.py
│   │   ├── merkle_root.py
│   │   └── README.md
│   ├── replay
│   │   ├── README.md
│   │   └── replay_receipt.py
│   ├── .gitkeep
│   ├── README.md
│   └── receipt.py
├── execution_plane
│   ├── sandbox_runner
│   │   └── README.md
│   └── README.md
├── experiments
│   ├── admissibility
│   │   ├── pressure_ramp
│   │   │   ├── config.yaml
│   │   │   └── README.md
│   │   └── simple_test
│   │       ├── .gitignore
│   │       ├── config.yaml
│   │       ├── README.md
│   │       └── run.py
│   ├── adversarial
│   │   └── mutation_injection
│   │       └── config.yaml
│   ├── autonomous
│   │   └── autonomous_controller.py
│   ├── conflict
│   │   └── conflicting_proposals
│   │       └── README.md
│   ├── critical_ratio_campaign
│   │   ├── results
│   │   │   ├── baseline_comparison.json
│   │   │   ├── falsification_report.json
│   │   │   ├── phase_space_map.json
│   │   │   ├── README.md
│   │   │   └── validation_report.json
│   │   ├── _legacy_run_experiment.py
│   │   ├── baselines.py
│   │   ├── CLAIMS.md
│   │   ├── expanded_experiment_config.json
│   │   ├── expected_outputs.json
│   │   ├── experiment_config.json
│   │   ├── falsification_tests.py
│   │   ├── merge_shards.py
│   │   ├── protocol.md
│   │   ├── README.md
│   │   ├── run_expanded_experiment.py
│   │   ├── run_experiment.py
│   │   ├── validate_results.py
│   │   └── visualize_phase_space.py
│   ├── evaluation_suite
│   │   └── run_eval.py
│   └── interaction
│       └── two_entity_exchange
│           └── README.md
├── failed_bundles
│   ├── .gitkeep
│   ├── auto_bundle_feedback.zip
│   ├── auto_bundle_fix_v2.zip
│   ├── auto_bundle_fix_v4.zip
│   ├── auto_bundle_fix_v5.zip
│   ├── auto_bundle_fix_v6.zip
│   ├── auto_bundle_fix_v7.zip
│   ├── auto_bundle_fix_v8.zip
│   ├── auto_bundle_observability_v1.zip
│   ├── auto_rollback_bundle_v1.zip
│   ├── bootstrap_and_convergence_bundles.zip
│   ├── coherent_experience_model_v1.zip
│   ├── constraint_min_bundle.zip
│   ├── constraint_min_bundle_v2.zip
│   ├── content_post_generation_bundle_v1.zip
│   ├── contract_snapshot_bundle_v1.zip
│   ├── control_plane_observability_v16.zip
│   ├── critical_ratio_campaign_bundle_v1.zip
│   ├── crypto_bot_v0_2_bundle.zip
│   ├── crypto_bot_v0_3_bundle.zip
│   ├── crypto_bot_v0_4_bundle.zip
│   ├── crypto_signing_v9_bundle.zip
│   ├── docs_aware_ingestion_bundle_v1.zip
│   ├── document_compression_bundle_v1.zip
│   ├── entity-sandbox-runner-deployment-bundle.zip
│   ├── entity-sandbox-runner-v2.zip
│   ├── execution_policy_engine_bundle_v1.zip
│   ├── full_governance_integration_bundle_v1.zip
│   ├── generator_v2_bundle.zip
│   ├── generator_v3_bundle.zip
│   ├── generator_v4_bundle.zip
│   ├── generator_v6_bundle.zip
│   ├── generator_v7_bundle.zip
│   ├── generator_v8_bundle.zip
│   ├── governed_agent_passport_v1_bundle_v1.zip
│   ├── governed_agent_passport_v1_ingestion_bundle.zip
│   ├── governed_agent_passport_v2_bundle.zip
│   ├── hard_rollback_bundle_v1.zip
│   ├── history_layer_bundle_v1.zip
│   ├── llm_adapter_readme_bundle_v1.zip
│   ├── master_workflow_v2_bundle.zip
│   ├── multi_agent_verification_v7_bundle.zip
│   ├── multi_platform_post_bundle_v1.zip
│   ├── passport_receipt_chain_v3_bundle.zip
│   ├── predictive_layer_v19.zip
│   ├── publishable_demo_export_bundle_v1.zip
│   ├── relationship_conditioned_execution_v1_1.zip
│   ├── relationship_conditioned_execution_v1_1_full.zip
│   ├── relationship_conditioned_execution_v1_2.zip
│   ├── relationship_conditioned_execution_v1_3.zip
│   ├── relationship_conditioned_execution_v1_4.zip
│   ├── relationship_conditioned_execution_v1_5.zip
│   ├── relationship_conditioned_execution_v2_0.zip
│   ├── relationship_conditioned_execution_v2_1.zip
│   ├── rollback_trigger_bundle_v1.zip
│   ├── safe_mode_bundle_v1.zip
│   ├── sandbox_981_1030_v1.zip
│   ├── sandbox_autonomous_loop_stabilization_v1.zip
│   ├── sandbox_bootstrap_permission_unlock_bundle_v1.zip
│   ├── sandbox_closed_loop_activation_v1.zip
│   ├── sandbox_convergence_bundle_v1.zip
│   ├── sandbox_convergence_bundle_v1_fix1.zip
│   ├── sandbox_convergence_full_memory_bundle_v1.zip
│   ├── sandbox_eval_ready_bundle.zip
│   ├── sandbox_eval_wiring_patch_v6_1.zip
│   ├── sandbox_next_50_upgrades_v4.zip
│   ├── sandbox_platform_bundle_v1_1.zip
│   ├── sandbox_research_grade_upgrades_1031_1040_v1.zip
│   ├── sandbox_run_workflow_upgrade_bundle_v1.zip
│   ├── sandbox_v11_1_to_12_bundle.zip
│   ├── sandbox_v14_3_to_v15_bundle.zip
│   ├── sandbox_v6_2_shared_state_patch.zip
│   ├── sandbox_v6_3_workflow_bundle.zip
│   ├── sandbox_v6_4_unified_promotion_bundle.zip
│   ├── sandbox_v6_5_no_cli_automation_bundle.zip
│   ├── sandbox_v7_1_stabilization_bundle.zip
│   ├── sandbox_v7_2_autonomous_persistence_bundle.zip
│   ├── sandbox_v7_6_to_7_9_bundle.zip
│   ├── sandbox_v7_autonomous_loop_bundle.zip
│   ├── sandbox_v8_1_to_8_5_bundle.zip
│   ├── sandbox_v8_governed_system_bundle.zip
│   ├── sandbox_v9_1_to_10_bundle.zip
│   ├── secure_bundle_integrity_bundle_v1.zip
│   ├── self_healing_loop_v6_bundle.zip
│   ├── self_improve_bundle_v1.zip
│   ├── stability_gate_v1.zip
│   ├── stability_gate_v10.zip
│   ├── stability_gate_v12.zip
│   ├── stability_gate_v13.zip
│   ├── stability_gate_v2.zip
│   ├── stability_gate_v3.zip
│   ├── stability_gate_v4.zip
│   ├── stability_gate_v5.zip
│   ├── stability_gate_v6.zip
│   ├── stability_gate_v7.zip
│   ├── stability_gate_v8.zip
│   ├── stability_gate_v9.zip
│   ├── stegcge_closure_modules_v1_bundle.zip
│   ├── stegdb_observability_bundle.zip
│   ├── stegghost-agent-simulation-lab.zip
│   ├── stegverse-dual-repo-bundle.zip
│   ├── stegverse-guardian-runtime.zip
│   ├── stegverse_architecture_aligned_bundle_v3.zip
│   ├── stegverse_ingestion_safe_recovery_bundle_v1.zip
│   ├── stegverse_spec_bundle_v1_1.zip
│   ├── stegverse_spec_bundle_v1_2.zip
│   ├── tc_tvc_platform_v0_2.zip
│   ├── tc_tvc_scaffolding_v0_1.zip
│   ├── token_economics_v1.zip
│   ├── token_economics_v10.zip
│   ├── token_economics_v10_manifest_fixed.zip
│   ├── token_economics_v11.zip
│   ├── token_economics_v12.zip
│   ├── token_economics_v13.zip
│   ├── token_economics_v14.zip
│   ├── token_economics_v15.zip
│   ├── token_economics_v2.zip
│   ├── token_economics_v3.zip
│   ├── token_economics_v4.zip
│   ├── token_economics_v5.zip
│   ├── token_economics_v6.zip
│   ├── token_economics_v7.zip
│   ├── token_economics_v8.zip
│   ├── token_economics_v9.zip
│   ├── tokenized_governance_bundle_v1.zip
│   ├── trajectory_aware_retry_v10_bundle.zip
│   ├── trajectory_engine_v5_bundle.zip
│   ├── tvc_export_bundle.zip
│   ├── ui_advanced_v18.zip
│   ├── ui_advanced_v18_manifest_fixed.zip
│   ├── ui_dashboard_control_v17.zip
│   ├── ui_dashboard_control_v17_manifest_fixed.zip
│   ├── v13_1_to_v14_bundle.zip
│   ├── v21_1_gatekeeper_bundle.zip
│   ├── v21_1B_ingestion_hardening_bundle.zip
│   ├── v21_1B_ingestion_hardening_bundle_fixed.zip
│   ├── v21_1C_ultra_compatible_ingestion_bootstrap_bundle.zip
│   ├── v21_2_formal_document_engine_bundle.zip
│   └── v21_to_v30_bundle.zip
├── federation_plane
│   ├── cross_lab_verification_router.py
│   ├── cross_node_campaign_dispatcher.py
│   ├── dataset_sync_scheduler.py
│   ├── distributed_claim_consensus.py
│   ├── federation_manifest.json
│   ├── federation_node_registry.py
│   ├── network_health_broadcaster.py
│   ├── peer_receipt_ledger_bridge.py
│   ├── peer_result_ingestor.py
│   ├── peer_validation_registry.py
│   └── remote_artifact_notary.py
├── gap_bundle_src
│   ├── config
│   │   └── authority_policy.json
│   ├── docs
│   │   └── GAP_SPEC.md
│   ├── install
│   │   ├── admission_engine.py
│   │   ├── execution_wrapper.py
│   │   ├── governed_passport.py
│   │   └── receipt_chain.py
│   ├── bundle_manifest.json
│   └── README.md
├── github_workflows
│   ├── autonomous_loop.yml
│   ├── autonomous_v10.yml
│   ├── autonomous_v12.yml
│   ├── autonomous_v15.yml
│   └── v30.yml
├── global_registry
│   ├── cross_lab_invariant_index.py
│   ├── dataset_provenance_registry.py
│   ├── evidence_chain_linker.py
│   ├── export_bundle_registry.py
│   ├── future_roadmap_783_900.json
│   ├── global_confidence_estimator.py
│   ├── global_uc_estimate_tracker.py
│   ├── invariant_registry_core.py
│   ├── invariant_version_tracker.py
│   ├── multi_scale_invariant_map.py
│   ├── registry_audit_log.py
│   ├── run_receipt_registry.py
│   └── theorem_candidate_registry.py
├── identity_plane
│   ├── artifact_watermark_stub.py
│   ├── compute_capacity_exchange.py
│   ├── cross_lab_contract_registry.py
│   ├── dataset_quality_scoreboard.py
│   ├── identity_resolution_api_stub.py
│   ├── marketplace_dispute_tracker.py
│   ├── marketplace_health_dashboard.py
│   ├── peer_reputation_verifier.py
│   ├── permissioned_download_gate.py
│   ├── research_collaboration_board.py
│   └── trust_anchor_manager.py
├── incoming_bundles
│   ├── .gitkeep
│   ├── auto_bundle_feedback.zip
│   └── governed_agent_passport_v1_ingestion_bundle.sha256
├── ingestion
│   ├── runtime
│   │   └── ingest_engine.py
│   ├── __init__.py
│   ├── bootstrap_install.py
│   ├── capability_validator.py
│   ├── classify_bundle_contents.py
│   ├── compare_workflows.py
│   ├── create_workflow_pr.py
│   ├── enforce_capabilities.py
│   ├── enforce_manifest.py
│   ├── find_all_bundles.py
│   ├── find_latest_bundle.py
│   ├── ingest_bundle.py
│   ├── json_safe.py
│   ├── module_registry.py
│   ├── move_processed_bundle.py
│   ├── orchestrator.py
│   ├── README.md
│   ├── validate_bundle_manifest.py
│   ├── verify_installation.py
│   ├── verify_signature.py
│   └── write_install_report.py
├── ingestion_backups
│   ├── .gitkeep
│   ├── __init__.py
│   ├── __init___1.py
│   ├── __init___2.py
│   ├── __init___3.py
│   ├── __init___4.py
│   ├── __init___5.py
│   ├── __init___6.py
│   ├── __init___7.py
│   ├── __init___8.py
│   ├── adaptive_boundary_targeter.py
│   ├── adaptive_campaign_auditor.py
│   ├── adaptive_information_budgeter.py
│   ├── adaptive_scheduler.py
│   ├── adaptive_scheduler_1.py
│   ├── adaptive_scheduler_10.py
│   ├── adaptive_scheduler_100.py
│   ├── adaptive_scheduler_101.py
│   ├── adaptive_scheduler_102.py
│   ├── adaptive_scheduler_103.py
│   ├── adaptive_scheduler_104.py
│   ├── adaptive_scheduler_105.py
│   ├── adaptive_scheduler_106.py
│   ├── adaptive_scheduler_107.py
│   ├── adaptive_scheduler_108.py
│   ├── adaptive_scheduler_109.py
│   ├── adaptive_scheduler_11.py
│   ├── adaptive_scheduler_110.py
│   ├── adaptive_scheduler_111.py
│   ├── adaptive_scheduler_112.py
│   ├── adaptive_scheduler_113.py
│   ├── adaptive_scheduler_114.py
│   ├── adaptive_scheduler_115.py
│   ├── adaptive_scheduler_116.py
│   ├── adaptive_scheduler_117.py
│   ├── adaptive_scheduler_118.py
│   ├── adaptive_scheduler_119.py
│   ├── adaptive_scheduler_12.py
│   ├── adaptive_scheduler_120.py
│   ├── adaptive_scheduler_121.py
│   ├── adaptive_scheduler_122.py
│   ├── adaptive_scheduler_123.py
│   ├── adaptive_scheduler_124.py
│   ├── adaptive_scheduler_125.py
│   ├── adaptive_scheduler_126.py
│   ├── adaptive_scheduler_127.py
│   ├── adaptive_scheduler_128.py
│   ├── adaptive_scheduler_129.py
│   ├── adaptive_scheduler_13.py
│   ├── adaptive_scheduler_130.py
│   ├── adaptive_scheduler_131.py
│   ├── adaptive_scheduler_132.py
│   ├── adaptive_scheduler_133.py
│   ├── adaptive_scheduler_134.py
│   ├── adaptive_scheduler_135.py
│   ├── adaptive_scheduler_136.py
│   ├── adaptive_scheduler_137.py
│   ├── adaptive_scheduler_138.py
│   ├── adaptive_scheduler_139.py
│   ├── adaptive_scheduler_14.py
│   ├── adaptive_scheduler_140.py
│   ├── adaptive_scheduler_141.py
│   ├── adaptive_scheduler_142.py
│   ├── adaptive_scheduler_143.py
│   ├── adaptive_scheduler_144.py
│   ├── adaptive_scheduler_145.py
│   ├── adaptive_scheduler_146.py
│   ├── adaptive_scheduler_147.py
│   ├── adaptive_scheduler_148.py
│   ├── adaptive_scheduler_149.py
│   ├── adaptive_scheduler_15.py
│   ├── adaptive_scheduler_150.py
│   ├── adaptive_scheduler_151.py
│   ├── adaptive_scheduler_152.py
│   ├── adaptive_scheduler_153.py
│   ├── adaptive_scheduler_154.py
│   ├── adaptive_scheduler_155.py
│   ├── adaptive_scheduler_156.py
│   ├── adaptive_scheduler_157.py
│   ├── adaptive_scheduler_16.py
│   ├── adaptive_scheduler_17.py
│   ├── adaptive_scheduler_18.py
│   ├── adaptive_scheduler_19.py
│   ├── adaptive_scheduler_2.py
│   ├── adaptive_scheduler_20.py
│   ├── adaptive_scheduler_21.py
│   ├── adaptive_scheduler_22.py
│   ├── adaptive_scheduler_23.py
│   ├── adaptive_scheduler_24.py
│   ├── adaptive_scheduler_25.py
│   ├── adaptive_scheduler_26.py
│   ├── adaptive_scheduler_27.py
│   ├── adaptive_scheduler_28.py
│   ├── adaptive_scheduler_29.py
│   ├── adaptive_scheduler_3.py
│   ├── adaptive_scheduler_30.py
│   ├── adaptive_scheduler_31.py
│   ├── adaptive_scheduler_32.py
│   ├── adaptive_scheduler_33.py
│   ├── adaptive_scheduler_34.py
│   ├── adaptive_scheduler_35.py
│   ├── adaptive_scheduler_36.py
│   ├── adaptive_scheduler_37.py
│   ├── adaptive_scheduler_38.py
│   ├── adaptive_scheduler_39.py
│   ├── adaptive_scheduler_4.py
│   ├── adaptive_scheduler_40.py
│   ├── adaptive_scheduler_41.py
│   ├── adaptive_scheduler_42.py
│   ├── adaptive_scheduler_43.py
│   ├── adaptive_scheduler_44.py
│   ├── adaptive_scheduler_45.py
│   ├── adaptive_scheduler_46.py
│   ├── adaptive_scheduler_47.py
│   ├── adaptive_scheduler_48.py
│   ├── adaptive_scheduler_49.py
│   ├── adaptive_scheduler_5.py
│   ├── adaptive_scheduler_50.py
│   ├── adaptive_scheduler_51.py
│   ├── adaptive_scheduler_52.py
│   ├── adaptive_scheduler_53.py
│   ├── adaptive_scheduler_54.py
│   ├── adaptive_scheduler_55.py
│   ├── adaptive_scheduler_56.py
│   ├── adaptive_scheduler_57.py
│   ├── adaptive_scheduler_58.py
│   ├── adaptive_scheduler_59.py
│   ├── adaptive_scheduler_6.py
│   ├── adaptive_scheduler_60.py
│   ├── adaptive_scheduler_61.py
│   ├── adaptive_scheduler_62.py
│   ├── adaptive_scheduler_63.py
│   ├── adaptive_scheduler_64.py
│   ├── adaptive_scheduler_65.py
│   ├── adaptive_scheduler_66.py
│   ├── adaptive_scheduler_67.py
│   ├── adaptive_scheduler_68.py
│   ├── adaptive_scheduler_69.py
│   ├── adaptive_scheduler_7.py
│   ├── adaptive_scheduler_70.py
│   ├── adaptive_scheduler_71.py
│   ├── adaptive_scheduler_72.py
│   ├── adaptive_scheduler_73.py
│   ├── adaptive_scheduler_74.py
│   ├── adaptive_scheduler_75.py
│   ├── adaptive_scheduler_76.py
│   ├── adaptive_scheduler_77.py
│   ├── adaptive_scheduler_78.py
│   ├── adaptive_scheduler_79.py
│   ├── adaptive_scheduler_8.py
│   ├── adaptive_scheduler_80.py
│   ├── adaptive_scheduler_81.py
│   ├── adaptive_scheduler_82.py
│   ├── adaptive_scheduler_83.py
│   ├── adaptive_scheduler_84.py
│   ├── adaptive_scheduler_85.py
│   ├── adaptive_scheduler_86.py
│   ├── adaptive_scheduler_87.py
│   ├── adaptive_scheduler_88.py
│   ├── adaptive_scheduler_89.py
│   ├── adaptive_scheduler_9.py
│   ├── adaptive_scheduler_90.py
│   ├── adaptive_scheduler_91.py
│   ├── adaptive_scheduler_92.py
│   ├── adaptive_scheduler_93.py
│   ├── adaptive_scheduler_94.py
│   ├── adaptive_scheduler_95.py
│   ├── adaptive_scheduler_96.py
│   ├── adaptive_scheduler_97.py
│   ├── adaptive_scheduler_98.py
│   ├── adaptive_scheduler_99.py
│   ├── adaptive_shard_reweighting_engine.py
│   ├── admission_engine.py
│   ├── aggregate_builder.py
│   ├── always_on_scheduler.py
│   ├── anomaly.py
│   ├── anomaly_1.py
│   ├── anomaly_2.py
│   ├── anomaly_3.py
│   ├── anomaly_4.py
│   ├── anomaly_5.py
│   ├── anomaly_6.py
│   ├── anomaly_7.py
│   ├── anomaly_8.py
│   ├── anomaly_9.py
│   ├── apply.py
│   ├── apply_1.py
│   ├── apply_2.py
│   ├── apply_3.py
│   ├── apply_4.py
│   ├── arbitration.py
│   ├── arbitration_1.py
│   ├── arbitration_2.py
│   ├── arbitration_3.py
│   ├── arbitration_4.py
│   ├── arbitration_5.py
│   ├── arbitration_6.py
│   ├── arbitration_7.py
│   ├── arbitration_8.py
│   └── arbitration_9.py
├── ingestion_reports
│   ├── bundle_docs
│   │   └── ingestion_tmp_README.md
│   ├── .gitkeep
│   ├── actuator_bridge_bundle_v1A.zip_20260319_044702.json
│   ├── adaptive_priority_engine_bundle_v1.zip_20260319_042855.json
│   ├── anomaly_detection_bundle_v1.zip_20260319_151227.json
│   ├── anomaly_detection_workflow_bundle_v1.zip_20260319_151822.json
│   ├── auto_bundle_feedback.zip_20260322_183058.json
│   ├── auto_bundle_feedback.zip_20260322_214849.json
│   ├── auto_bundle_feedback.zip_20260322_230637.json
│   ├── auto_bundle_fix_v1.zip_20260322_194315.json
│   ├── auto_bundle_fix_v3.zip_20260322_204342.json
│   ├── auto_bundle_observability_v1.zip_20260322_205756.json
│   ├── autonomous_loop_orchestrator_bundle_v1.zip_20260319_040844.json
│   ├── autonomous_loop_workflow_bundle_v1.zip_20260319_041225.json
│   ├── bootstrap_and_convergence_bundles.zip_20260324_152313.json
│   ├── bundle_manifest_standard_bundle_install_report.json
│   ├── canonical_core_reset_bundle_v2.zip_20260319_234536.json
│   ├── canonical_feedback_bundle_v1.zip_20260319_032102.json
│   ├── canonical_feedback_runner_bundle_v1.zip_20260319_032944.json
│   ├── canonical_receipt_binder_bundle_v1.zip_20260319_035044.json
│   ├── coherent_experience_model_v1.zip_20260319_010641.json
│   ├── coherent_experience_model_v1_fixed.zip_20260319_010958.json
│   ├── constraint_min_bundle.zip_20260322_032235.json
│   ├── constraint_min_bundle_v2.zip_20260322_032436.json
│   ├── constraint_min_bundle_v3.zip_20260322_032801.json
│   ├── control_plane_observability_v16.zip_20260322_230637.json
│   ├── control_plane_observability_v16.zip_20260323_045741.json
│   ├── critical_ratio_campaign_bundle_v1.zip_20260316_213156.json
│   ├── critical_ratio_campaign_bundle_v2.zip_20260316_220143.json
│   ├── critical_ratio_campaign_bundle_v2.zip_20260316_232040.json
│   ├── critical_ratio_runner_files_v1.zip_20260317_041443.json
│   ├── crypto_bot_v0_2_bundle.zip_20260323_150729.json
│   ├── crypto_bot_v0_2_bundle.zip_20260324_145801.json
│   ├── crypto_bot_v0_3_bundle.zip_20260324_150338.json
│   ├── crypto_signing_v9_bundle.zip_20260322_205756.json
│   ├── distributed_worker_bundle_v1.zip_20260319_043009.json
│   ├── docs_aware_ingestion_bundle_v1.zip_20260318_214317.json
│   ├── document_compression_bundle_v1.zip_20260319_025916.json
│   ├── document_compression_bundle_v1A_minimal.zip_20260319_030808.json
│   ├── entity-sandbox-runner-v2.zip_20260323_150729.json
│   ├── entity-sandbox-runner-v2.zip_20260324_145801.json
│   ├── entity_sandbox_runner_github_bundle_install_report.json
│   ├── execution_policy_engine_bundle_v1.zip_20260319_043848.json
│   ├── execution_policy_engine_bundle_v1A.zip_20260319_044340.json
│   ├── failure_feedback_loop_bundle_v1.zip_20260322_051311.json
│   ├── failure_recovery_bundle_v1.zip_20260319_042444.json
│   ├── feedback_execution_bridge_bundle_v1.zip_20260319_040404.json
│   ├── feedback_injection_bundle_v1.zip_20260319_035408.json
│   ├── full_governance_integration_bundle_v1.zip_20260322_205757.json
│   ├── generator_v2_bundle.zip_20260322_210954.json
│   ├── generator_v2_bundle.zip_20260322_214850.json
│   ├── generator_v2_bundle.zip_20260322_220130.json
│   ├── generator_v2_bundle.zip_20260322_230637.json
│   ├── generator_v3_bundle.zip_20260322_214850.json
│   ├── generator_v3_bundle.zip_20260322_220130.json
│   ├── generator_v3_bundle.zip_20260322_230637.json
│   ├── generator_v4_bundle.zip_20260322_214850.json
│   ├── generator_v4_bundle.zip_20260322_220130.json
│   ├── generator_v4_bundle.zip_20260322_230637.json
│   ├── generator_v6_bundle.zip_20260323_150729.json
│   ├── generator_v6_bundle.zip_20260324_145801.json
│   ├── generator_v7_bundle.zip_20260323_150729.json
│   ├── generator_v7_bundle.zip_20260324_145801.json
│   ├── generator_v8_bundle.zip_20260323_150729.json
│   ├── generator_v8_bundle.zip_20260324_145801.json
│   ├── goal_directed_execution_bundle_v1A.zip_20260319_044618.json
│   ├── governed_agent_passport_v1_bundle_v1.zip_20260322_195107.json
│   ├── governed_agent_passport_v2_bundle.zip_20260322_204342.json
│   ├── hard_rollback_bundle_v1.zip_20260324_150338.json
│   ├── ingestion.log
│   ├── iphone_no_cli_promoter_workflow_bundle.zip_20260318_222023.json
│   ├── knowledge_delta_bundle_v1.zip_20260319_033022.json
│   ├── llm_adapter_readme_bundle_v1.zip_20260320_042940.json
│   ├── llm_adapter_readme_bundle_v2.zip_20260320_043316.json
│   ├── marketing_system_bundle_v1.zip_20260319_151823.json
│   ├── marketing_workflow_bundle_v1.zip_20260319_152954.json
│   ├── marketing_workflow_bundle_v1.zip_20260319_234536.json
│   ├── multi_agent_verification_v7_bundle.zip_20260322_205757.json
│   ├── passport_receipt_chain_v3_bundle.zip_20260322_205757.json
│   ├── path_safety_upgrade_bundle_install_report.json
│   ├── pattern_memory_bundle_v1A.zip_20260319_044440.json
│   ├── predictive_layer_v19.zip_20260322_230637.json
│   ├── predictive_layer_v19.zip_20260323_045741.json
│   ├── preflight_guard_bundle_v1.zip_20260319_081336.json
│   ├── priority_router_bundle_v1.zip_20260322_055214.json
│   ├── promotion_receipts_diff_visibility_bundle_v1.zip_20260318_225828.json
│   ├── promotion_receipts_diff_visibility_bundle_v1.zip_20260318_231602.json
│   ├── promotion_receipts_diff_visibility_bundle_v1.zip_20260319_010641.json
│   ├── publishable_demo_export_bundle_v1.zip_20260317_090914.json
│   ├── publishable_demo_export_bundle_v1.zip_20260317_104642.json
│   ├── relationship_conditioned_execution_v1_1_full.zip_20260322_231225.json
│   ├── repo_readme_update_bundle_v2.zip_20260318_215136.json
│   ├── repo_root_promoter_bundle_v1.zip_20260318_221343.json
│   ├── rollback_engine_bundle_v1.zip_20260319_081756.json
│   ├── runtime_ledger_replay_bundle_v0_1.zip_20260315_164705.json
│   ├── safe_ingestion_upgrade_bundle_install_report.json
│   ├── sandbox_901_930_v1.zip_20260317_053055.json
│   ├── sandbox_901_930_v1.zip_20260317_090745.json
│   ├── sandbox_981_1030_v1.zip_20260317_090745.json
│   ├── sandbox_autonomous_loop_stabilization_v1.zip_20260317_090745.json
│   ├── sandbox_autonomous_research_upgrades_583_602_v1.zip_20260317_004252.json
│   ├── sandbox_closed_loop_activation_v1.zip_20260317_090745.json
│   ├── sandbox_convergence_bundle_v1.zip_20260324_145801.json
│   ├── sandbox_convergence_bundle_v1_fix1.zip_20260324_150339.json
│   ├── sandbox_distributed_research_upgrades_643_682_v1.zip_20260317_031645.json
│   ├── sandbox_docs_manifest_bundle_v1.zip_20260316_211736.json
│   ├── sandbox_future_upgrades_783_900_v1.zip_20260317_051044.json
│   ├── sandbox_future_upgrades_783_900_v1.zip_20260317_090745.json
│   ├── sandbox_invariant_discovery_upgrades_603_642_v1.zip_20260317_004503.json
│   ├── sandbox_next_50_upgrades_v4.zip_20260317_143110.json
│   ├── sandbox_platform_bundle_v1_1.zip_20260315_152814.json
│   ├── sandbox_platform_bundle_v1_2.zip_20260315_155518.json
│   ├── sandbox_readme_updates_v1.zip_20260316_172102.json
│   ├── sandbox_readme_updates_v1.zip_20260316_195358.json
│   ├── sandbox_readme_updates_v2.zip_20260316_195358.json
│   ├── sandbox_research_grade_upgrades_1031_1040_v1.zip_20260317_093518.json
│   ├── sandbox_research_grade_upgrades_1031_1040_v1.zip_20260317_104642.json
│   ├── sandbox_research_upgrades_106_115_v1.zip_20260316_161208.json
│   ├── sandbox_research_upgrades_116_125_v1.zip_20260316_164142.json
│   ├── sandbox_research_upgrades_126_135_v1.zip_20260316_164142.json
│   ├── sandbox_research_upgrades_136_150_v1.zip_20260316_164142.json
│   ├── sandbox_research_upgrades_151_165_v1.zip_20260316_172248.json
│   ├── sandbox_research_upgrades_166_180_v1.zip_20260316_172102.json
│   ├── sandbox_research_upgrades_181_195_v1.zip_20260316_172102.json
│   ├── sandbox_research_upgrades_196_210_v1.zip_20260316_172103.json
│   ├── sandbox_research_upgrades_211_225_v1.zip_20260316_172103.json
│   ├── sandbox_research_upgrades_226_260_v1.zip_20260316_172103.json
│   ├── sandbox_research_upgrades_261_290_v1.zip_20260316_195358.json
│   ├── sandbox_research_upgrades_291_330_v1.zip_20260316_195359.json
│   ├── sandbox_research_upgrades_331_360_v1.zip_20260316_195359.json
│   ├── sandbox_research_upgrades_361_390_v1.zip_20260316_195359.json
│   ├── sandbox_research_upgrades_391_420_v1.zip_20260316_195359.json
│   ├── sandbox_research_upgrades_421_450_v1.zip_20260316_195359.json
│   ├── sandbox_research_upgrades_91_105_v1.zip_20260316_154824.json
│   ├── sandbox_run_workflow_upgrade_bundle_v1.zip_20260317_004109.json
│   ├── sandbox_run_workflow_upgrade_bundle_v2.zip_20260317_031645.json
│   ├── sandbox_service_and_validation_upgrades_483_502_v1.zip_20260316_214723.json
│   ├── sandbox_service_and_validation_upgrades_483_502_v1.zip_20260316_220143.json
│   ├── sandbox_service_and_validation_upgrades_483_502_v1.zip_20260316_232040.json
│   ├── sandbox_service_and_validation_upgrades_503_517_v1.zip_20260316_232040.json
│   ├── sandbox_service_and_validation_upgrades_503_517_v1.zip_20260316_235630.json
│   ├── sandbox_service_and_validation_upgrades_503_542_v1.zip_20260316_235630.json
│   ├── sandbox_service_and_validation_upgrades_543_562_v1.zip_20260317_003857.json
│   ├── sandbox_service_and_validation_upgrades_563_582_v1.zip_20260317_003858.json
│   ├── sandbox_service_upgrades_451_482_v1.zip_20260316_195359.json
│   ├── sandbox_upgrades_683_732_v1.zip_20260317_031645.json
│   ├── sandbox_v4_fixed.zip_20260317_144523.json
│   ├── sandbox_v5_fixed.zip_20260317_144523.json
│   ├── sandbox_v6_fixed.zip_20260317_144653.json
│   ├── secure_bundle_integrity_bundle_v1.zip_20260322_204342.json
│   ├── self_healing_loop_v6_bundle.zip_20260322_205757.json
│   ├── self_improve_bundle_v1.zip_20260322_042138.json
│   ├── self_improve_bundle_v3.zip_20260322_043812.json
│   ├── self_improve_bundle_v4.zip_20260322_044609.json
│   ├── self_modifying_loop_bundle_v1A.zip_20260319_044532.json
│   ├── shard_reliability_lock_bundle_v1.zip_20260317_051927.json
│   ├── shard_reliability_lock_bundle_v1.zip_20260317_090745.json
│   ├── stability_gate_v1.zip_20260322_205757.json
│   ├── stability_gate_v10.zip_20260322_220130.json
│   ├── stability_gate_v10.zip_20260322_230637.json
│   ├── stability_gate_v12.zip_20260323_150729.json
│   ├── stability_gate_v3.zip_20260322_205757.json
│   ├── stability_gate_v5.zip_20260322_205757.json
│   ├── stability_gate_v8.zip_20260322_214850.json
│   ├── state_delta_uncertainty_bundle_v1.zip_20260318_231602.json
│   ├── state_delta_uncertainty_bundle_v1.zip_20260319_010641.json
│   ├── state_scoring_bundle_v1.zip_20260319_151227.json
│   ├── state_scoring_workflow_bundle_v1.zip_20260319_151823.json
│   ├── stegcge_closure_modules_v1_bundle.zip_20260321_225647.json
│   ├── stegdb_observability_bundle.zip_20260323_150730.json
│   ├── stegdb_observability_bundle.zip_20260324_145801.json
│   ├── stegghost-agent-simulation-lab.zip_20260323_045741.json
│   ├── stegverse-dual-repo-bundle.zip_20260323_045741.json
│   ├── stegverse_architecture_aligned_bundle_v3.zip_20260317_105018.json
│   ├── stegverse_architecture_aligned_bundle_v3.zip_20260317_143110.json
│   ├── stegverse_experiment_fix_bundle_v1.zip_20260317_043439.json
│   ├── stegverse_ingestion_safe_recovery_bundle_v1.zip_20260317_103850.json
│   ├── stegverse_ingestion_safe_recovery_bundle_v2.zip_20260317_104444.json
│   ├── stegverse_multi_entity_sim_bundle_install_report.json
│   ├── stegverse_observatory_upgrade_bundle_install_report.json
│   ├── stegverse_result_delivery_bundle_v1.zip_20260316_232040.json
│   ├── stegverse_result_delivery_bundle_v1.zip_20260316_235630.json
│   ├── stegverse_sandbox_combined_bundle_v1.zip_20260316_213156.json
│   ├── stegverse_spec_bundle_v1_2.zip_20260324_150339.json
│   ├── tc_tvc_platform_v0_2.zip_20260315_150859.json
│   ├── tc_tvc_platform_v0_2.zip_20260315_151757.json
│   ├── tc_tvc_scaffolding_v0_1.zip_20260315_135248.json
│   ├── token_economics_v1.zip_20260322_230637.json
│   ├── token_economics_v10.zip_20260322_230637.json
│   ├── token_economics_v11.zip_20260322_230637.json
│   ├── token_economics_v12.zip_20260322_230637.json
│   ├── token_economics_v13.zip_20260322_230637.json
│   ├── token_economics_v14.zip_20260322_230637.json
│   ├── token_economics_v15.zip_20260322_230638.json
│   ├── token_economics_v2.zip_20260322_230638.json
│   ├── token_economics_v3.zip_20260322_230638.json
│   ├── token_economics_v4.zip_20260322_230638.json
│   ├── token_economics_v5.zip_20260322_230638.json
│   ├── token_economics_v6.zip_20260322_230638.json
│   └── token_economics_v7.zip_20260322_230638.json
├── install
│   ├── engine
│   │   ├── admission_engine_v4.py
│   │   ├── agent_roles.py
│   │   ├── anchor_engine.py
│   │   ├── authority_gate.py
│   │   ├── authority_policy.py
│   │   ├── bootstrap_permission_unlock.py
│   │   ├── bundle_inventory_engine.py
│   │   ├── challenge_engine.py
│   │   ├── closure_engine.py
│   │   ├── competition_engine.py
│   │   ├── conflict.py
│   │   ├── consensus.py
│   │   ├── consensus_engine.py
│   │   ├── consensus_gate.py
│   │   ├── contract_snapshot.py
│   │   ├── core.py
│   │   ├── distributed_validation.py
│   │   ├── economic_consensus.py
│   │   ├── economic_gate.py
│   │   ├── economic_incentives.py
│   │   ├── emission_controller.py
│   │   ├── execute_next_action.py
│   │   ├── execution_pipeline_v4.py
│   │   ├── failure_feedback.py
│   │   ├── full_system_memory.py
│   │   ├── gcat_bcat_evaluator.py
│   │   ├── governance_consensus_extension.py
│   │   ├── governance_multi_sig_extension.py
│   │   ├── governance_pipeline_ext.py
│   │   ├── governance_receipt.py
│   │   ├── history_engine.py
│   │   ├── key_lifecycle.py
│   │   ├── llm_self_improve.py
│   │   ├── multi_sig_policy.py
│   │   ├── multi_sig_verify.py
│   │   ├── multi_step_planner.py
│   │   ├── next_action_engine.py
│   │   ├── plan_memory.py
│   │   ├── priority_router.py
│   │   ├── proposal_to_bundle.py
│   │   ├── receipt_chain.py
│   │   ├── receipt_reconciler.py
│   │   ├── registry.py
│   │   ├── repo_map_generator.py
│   │   ├── repo_snapshot.py
│   │   ├── self_improve_runner.py
│   │   ├── signed_receipts_v8.py
│   │   ├── slashing_rewards.py
│   │   ├── stake_registry.py
│   │   └── step_completion.py
│   ├── sim
│   │   └── simulation.py
│   ├── tests
│   │   ├── test_admission_engine_v4.py
│   │   ├── test_authority_policy.py
│   │   ├── test_auto_repair.py
│   │   ├── test_bootstrap_permission_unlock.py
│   │   ├── test_consensus.py
│   │   ├── test_contract_snapshot.py
│   │   ├── test_convergence_engine.py
│   │   ├── test_economic.py
│   │   ├── test_execution_pipeline_v4.py
│   │   ├── test_failure_feedback.py
│   │   ├── test_fix_missing_cge_root.py
│   │   ├── test_generator_v2.py
│   │   ├── test_history_engine.py
│   │   ├── test_internal_brain_chain.py
│   │   ├── test_manifest.py
│   │   ├── test_multi_sig.py
│   │   ├── test_multi_step_planner.py
│   │   ├── test_plan_memory.py
│   │   ├── test_priority_router.py
│   │   ├── test_receipt_chain.py
│   │   ├── test_receipts.py
│   │   ├── test_self_improve.py
│   │   ├── test_signed_receipts_v8.py
│   │   ├── test_slashing.py
│   │   ├── test_step_completion.py
│   │   └── test_v8.py
│   ├── .gitkeep
│   ├── __init__.py
│   ├── actuator_bridge.py
│   ├── adaptive_priority_engine.py
│   ├── adaptive_scheduler.py
│   ├── adversarial_filter.py
│   ├── agent_registry.py
│   ├── anchor.py
│   ├── anomaly.py
│   ├── anomaly_detection.py
│   ├── apply.py
│   ├── arbitration.py
│   ├── audit.py
│   ├── auth_scope.py
│   ├── authority_resolver.py
│   ├── autonomous_loop_orchestrator.py
│   ├── bcat_engine.py
│   ├── bundle_builder.py
│   ├── bundle_guard.py
│   ├── bundle_manifest.json
│   ├── canonical_feedback.py
│   ├── canonical_receipt_binder.py
│   ├── check_file_engine.py
│   ├── citation_engine.py
│   ├── compat_adapter.py
│   ├── consensus.py
│   ├── consensus_engine.py
│   ├── control_plane.py
│   ├── coordination.py
│   ├── cross_verify.py
│   ├── crypto.py
│   ├── crypto_keys.py
│   ├── decentralized_worker_runtime.py
│   ├── decision_state_recorder.py
│   ├── delta_decomposition.py
│   ├── deterministic_enforcer.py
│   ├── distributed_worker.py
│   ├── distributed_worker_network.py
│   ├── document_compactor.py
│   ├── document_engine.py
│   ├── document_pipeline.py
│   ├── drift.py
│   ├── economic_weighting.py
│   ├── escalation.py
│   ├── eval_metrics.py
│   ├── eval_orchestrator.py
│   ├── evidence_chain.py
│   ├── execution_policy_engine.py
│   ├── experience_engine.py
│   ├── external_connectors.py
│   ├── external_signal_adapter.py
│   ├── failure_recovery_runner.py
│   ├── feedback_execution_bridge.py
│   ├── feedback_injection.py
│   ├── finco.py
│   ├── goal_directed_execution.py
│   ├── ingestion_preprocessor.py
│   ├── ingestion_v2.py
│   ├── install_bundle.py
│   ├── install_bundle_autoregister.py
│   ├── install_platform.py
│   ├── install_runtime_ledger.py
│   ├── install_workflow.py
│   ├── knowledge_delta.py
│   ├── latex_renderer.py
│   ├── lifecycle_manager.py
│   ├── llm_adapter.py
│   ├── llm_gateway.py
│   ├── llm_weighting.py
│   ├── manifest_autofix.py
│   ├── marketing_system.py
│   ├── marketing_system_workflow.yml.txt
│   ├── network_registry.py
│   ├── node_consensus.py
│   ├── node_identity.py
│   ├── observability.py
│   ├── orchestrator.py
│   ├── orchestrator_hook.py
│   ├── pattern_memory.py
│   ├── pdf_renderer.py
│   ├── peer_verification.py
│   ├── policy_engine.py
│   ├── policy_loader.py
│   ├── policy_signature.py
│   ├── policy_voting.py
│   ├── precision_engine.py
│   ├── predictive_engine.py
│   ├── preflight_canonical.py
│   ├── preflight_guard.py
│   ├── preflight_strict.py
│   ├── promote_workflow.py
│   ├── proposal_adapter.py
│   ├── quorum.py
│   ├── quorum_consensus.py
│   ├── README.md
│   ├── receipt_chain.py
│   ├── receipt_guard.py
│   ├── receipt_logger.py
│   ├── receipt_stream.py
│   ├── recovery_loop.py
│   ├── remote_ingest.py
│   ├── remote_policy.py
│   ├── replay.py
│   ├── replay_guard.py
│   ├── repo_root_promoter.py
│   ├── reputation_decay.py
│   ├── rigel_guard.py
│   ├── rigel_invariant.py
│   ├── rigel_policy.py
│   ├── rollback_engine.py
│   ├── run_canonical_loop.py
│   ├── saas_enforcement.py
│   ├── safe_json.py
│   ├── self_healing_ingestion.py
│   ├── self_modifying_loop.py
│   ├── shard_scheduler.py
│   ├── signature_verifier.py
│   ├── snapshot_verification.py
│   ├── stability.py
│   ├── stability_governor.py
│   ├── state_delta_engine.py
│   ├── state_scoring.py
│   ├── system_state.py
│   ├── test_llm_adapter.py
│   ├── tool_contracts.py
│   ├── trust_consensus.py
│   ├── trust_engine.py
│   ├── u_signal_engine.py
│   ├── u_signal_integration.py
│   ├── unified_promotion_patch.py
│   ├── worker_node.py
│   ├── worker_registry.py
│   └── worker_scoring.py
├── installed_bundles
│   ├── .gitkeep
│   ├── actuator_bridge_bundle_v1A.zip
│   ├── adaptive_priority_engine_bundle_v1.zip
│   ├── admission_receipt_integration_v4_bundle.zip
│   ├── anomaly_detection_bundle_v1.zip
│   ├── anomaly_detection_workflow_bundle_v1.zip
│   ├── authority_scope_enforcement_bundle_v1.zip
│   ├── auto_bundle_feedback.zip
│   ├── auto_bundle_fix_v1.zip
│   ├── auto_bundle_fix_v3.zip
│   ├── autonomous_loop_orchestrator_bundle_v1.zip
│   ├── autonomous_loop_workflow_bundle_v1.zip
│   ├── autonomous_v20_1_preflight_bundle.zip
│   ├── bundle_manifest_standard_bundle.zip
│   ├── canonical_core_reset_bundle_v2.zip
│   ├── canonical_feedback_bundle_v1.zip
│   ├── canonical_feedback_runner_bundle_v1.zip
│   ├── canonical_receipt_binder_bundle_v1.zip
│   ├── coherent_experience_model_v1_fixed.zip
│   ├── consensus_layer_bundle_v1.zip
│   ├── constraint_min_bundle_v3.zip
│   ├── critical_ratio_campaign_bundle_v2.zip
│   ├── critical_ratio_runner_files_v1.zip
│   ├── distributed_worker_bundle_v1.zip
│   ├── document_compression_bundle_v1A_minimal.zip
│   ├── dsr_bundle_v2.zip
│   ├── economic_governance_bundle_v1.zip
│   ├── entity_sandbox_runner_github_bundle.zip
│   ├── entity_sandbox_runner_lifecycle_auth_bundle.zip
│   ├── execution_policy_engine_bundle_v1A.zip
│   ├── failure_feedback_loop_bundle_v1.zip
│   ├── failure_recovery_bundle_v1.zip
│   ├── feedback_execution_bridge_bundle_v1.zip
│   ├── feedback_injection_bundle_v1.zip
│   ├── goal_directed_execution_bundle_v1A.zip
│   ├── governance_advanced_bundle_v1.zip
│   ├── iphone_no_cli_promoter_workflow_bundle.zip
│   ├── knowledge_delta_bundle_v1.zip
│   ├── llm_adapter_readme_bundle_v2.zip
│   ├── marketing_system_bundle_v1.zip
│   ├── marketing_workflow_bundle_v1.zip
│   ├── multi_sig_enforcement_bundle_v1.zip
│   ├── multi_step_planner_bundle_v1.zip
│   ├── passport_receipt_chain_v3_bundle.zip
│   ├── path_safety_upgrade_bundle.zip
│   ├── pattern_memory_bundle_v1A.zip
│   ├── plan_memory_bundle_v1.zip
│   ├── preflight_guard_bundle_v1.zip
│   ├── priority_router_bundle_v1.zip
│   ├── promotion_receipts_diff_visibility_bundle_v1.zip
│   ├── repo_readme_update_bundle_v2.zip
│   ├── repo_root_promoter_bundle_v1.zip
│   ├── rollback_engine_bundle_v1.zip
│   ├── runtime_ledger_replay_bundle_v0_1.zip
│   ├── safe_ingestion_upgrade_bundle.zip
│   ├── sandbox_901_930_v1.zip
│   ├── sandbox_autonomous_research_upgrades_583_602_v1.zip
│   ├── sandbox_distributed_research_upgrades_643_682_v1.zip
│   ├── sandbox_docs_manifest_bundle_v1.zip
│   ├── sandbox_future_upgrades_783_900_v1.zip
│   ├── sandbox_invariant_discovery_upgrades_603_642_v1.zip
│   ├── sandbox_platform_bundle_v1_2.zip
│   ├── sandbox_readme_updates_v1.zip
│   ├── sandbox_readme_updates_v2.zip
│   ├── sandbox_research_upgrades_106_115_v1.zip
│   ├── sandbox_research_upgrades_116_125_v1.zip
│   ├── sandbox_research_upgrades_126_135_v1.zip
│   ├── sandbox_research_upgrades_136_150_v1.zip
│   ├── sandbox_research_upgrades_151_165_v1.zip
│   ├── sandbox_research_upgrades_166_180_v1.zip
│   ├── sandbox_research_upgrades_181_195_v1.zip
│   ├── sandbox_research_upgrades_196_210_v1.zip
│   ├── sandbox_research_upgrades_211_225_v1.zip
│   ├── sandbox_research_upgrades_226_260_v1.zip
│   ├── sandbox_research_upgrades_261_290_v1.zip
│   ├── sandbox_research_upgrades_291_330_v1.zip
│   ├── sandbox_research_upgrades_331_360_v1.zip
│   ├── sandbox_research_upgrades_361_390_v1.zip
│   ├── sandbox_research_upgrades_391_420_v1.zip
│   ├── sandbox_research_upgrades_421_450_v1.zip
│   ├── sandbox_research_upgrades_91_105_v1.zip
│   ├── sandbox_run_workflow_upgrade_bundle_v2.zip
│   ├── sandbox_service_and_validation_upgrades_483_502_v1.zip
│   ├── sandbox_service_and_validation_upgrades_503_517_v1.zip
│   ├── sandbox_service_and_validation_upgrades_503_542_v1.zip
│   ├── sandbox_service_and_validation_upgrades_543_562_v1.zip
│   ├── sandbox_service_and_validation_upgrades_563_582_v1.zip
│   ├── sandbox_service_upgrades_451_482_v1.zip
│   ├── sandbox_upgrades_683_732_v1.zip
│   ├── sandbox_v4_fixed.zip
│   ├── sandbox_v5_fixed.zip
│   ├── sandbox_v6_fixed.zip
│   ├── sandbox_v7_3_to_7_5_bundle.zip
│   ├── self_improve_bundle_v3.zip
│   ├── self_improve_bundle_v4.zip
│   ├── self_modifying_loop_bundle_v1A.zip
│   ├── shard_reliability_lock_bundle_v1.zip
│   ├── signed_receipts_v8_bundle.zip
│   ├── slashing_rewards_bundle_v1.zip
│   ├── state_delta_uncertainty_bundle_v1.zip
│   ├── state_scoring_bundle_v1.zip
│   ├── state_scoring_workflow_bundle_v1.zip
│   ├── stegverse_docs_bundle.zip
│   ├── stegverse_docs_v2_bundle.zip
│   ├── stegverse_experiment_fix_bundle_v1.zip
│   ├── stegverse_ingestion_safe_recovery_bundle_v2.zip
│   ├── stegverse_multi_entity_sim_bundle.zip
│   ├── stegverse_observatory_upgrade_bundle.zip
│   ├── stegverse_result_delivery_bundle_v1.zip
│   ├── stegverse_sandbox_combined_bundle_v1.zip
│   ├── step_completion_bundle_v1.zip
│   ├── token_economics_v3_manifest_fixed.zip
│   ├── v21_1_gatekeeper_bundle.zip
│   ├── v21_1A_ingestion_bootstrap_bundle.zip
│   ├── v21_1B_ingestion_hardening_bundle.zip
│   ├── v21_1B_ingestion_hardening_bundle_manifest_fixed.zip
│   ├── v21_1C_ultra_compatible_ingestion_bootstrap_bundle_manifest_fixed.zip
│   ├── v21_1D_dual_version_ultra_compatible_ingestion_bootstrap_bundle.zip
│   ├── v21_2A_formal_document_engine_bootstrap_bundle.zip
│   ├── v21_3A_publication_engine_bootstrap_bundle.zip
│   ├── v21_strict_system_bundle.zip
│   ├── v21_to_v30_bundle.zip
│   ├── workflow_repair_bundle.zip
│   └── workflow_review_classifier_bundle.zip
├── integrations
│   └── U_SIGNAL_INTEGRATION_NOTES.md
├── interaction_graph
│   ├── __init__.py
│   ├── graph_builder.py
│   └── graph_metrics.py
├── internal_brain
│   ├── actuator.py
│   ├── brain_runner.py
│   ├── closure_engine.py
│   ├── explorer.py
│   ├── internal_brain_actuator.py
│   ├── internal_brain_closure_engine.py
│   ├── internal_brain_explorer.py
│   ├── internal_brain_reconciler.py
│   └── reconciler.py
├── logs
│   ├── audit.json
│   ├── ingestion_log.json
│   ├── repo_root_promotions.json
│   └── state.json
├── manifests
│   └── README.md
├── marketing
│   ├── post_templates
│   │   ├── linkedin_system_insight.md
│   │   ├── substack_longform_template.md
│   │   └── x_thread_template.md
│   ├── scheduled_posts
│   │   └── next_posts.md
│   ├── .gitkeep
│   ├── content_log.json
│   └── strategy.md
├── marketplace_plane
│   ├── artifact_license_tracker.py
│   ├── compute_contributor_registry.py
│   ├── compute_offer_matcher.py
│   ├── consent_bound_export_gate.py
│   ├── contributor_payout_stub.py
│   ├── dataset_access_policy_engine.py
│   ├── dataset_contributor_registry.py
│   ├── dataset_exchange_registry.py
│   ├── dataset_usage_meter.py
│   ├── experiment_bid_router.py
│   ├── experiment_credit_ledger.py
│   ├── experiment_patronage_router.py
│   ├── grant_tracking_stub.py
│   ├── identity_audit_log.py
│   ├── marketplace_fee_router.py
│   ├── marketplace_listing_builder.py
│   ├── node_attestation_registry.py
│   ├── node_trust_scorecard.py
│   ├── policy_receipt_market_linker.py
│   ├── proof_of_replication_stub.py
│   ├── public_key_directory.py
│   ├── receipt_bound_identity_linker.py
│   ├── receipt_signature_exchange.py
│   ├── replication_reward_router.py
│   ├── researcher_identity_registry.py
│   ├── researcher_reputation_index.py
│   ├── sponsor_visibility_registry.py
│   ├── trust_badge_generator.py
│   └── trust_decay_monitor.py
├── multi_entity_sim
│   ├── adversary_agents.py
│   ├── coalition_engine.py
│   ├── governance_failure_detector.py
│   ├── simulation_engine.py
│   └── trust_propagation.py
├── observation_plane
│   ├── phase_space
│   │   └── README.md
│   ├── README.md
│   └── u_signal_monitor.py
├── observatory
│   ├── state_log
│   │   ├── record_runtime_event.py
│   │   ├── record_state.py
│   │   └── runtime_ledger.jsonl
│   ├── .gitkeep
│   ├── __init__.py
│   ├── adaptive_boundary_discovery_engine.py
│   ├── adaptive_campaign_controller.py
│   ├── adaptive_campaign_launcher.py
│   ├── adaptive_hypothesis_pruner.py
│   ├── adaptive_intervention_planner.py
│   ├── adaptive_model_refitter.py
│   ├── adaptive_rg_refinement.py
│   ├── adaptive_sampling_scorecard.py
│   ├── adaptive_shard_allocator.py
│   ├── adaptive_uc_refiner.py
│   ├── anomaly_cluster_detector.py
│   ├── anomaly_discovery_engine.py
│   ├── anomaly_root_cause_analyzer.py
│   ├── automated_dataset_curator.py
│   ├── automated_null_hypothesis_tester.py
│   ├── automated_research_report_builder.py
│   ├── autonomous_campaign_scheduler.py
│   ├── autonomous_dataset_refiner.py
│   ├── autonomous_experiment_generator.py
│   ├── autonomous_research_cycle_manager.py
│   ├── autonomous_research_supervisor.py
│   ├── autonomous_theorem_publisher.py
│   ├── autonomous_theory_director.py
│   ├── beta_tracking_engine.py
│   ├── bootstrap_validation_engine.py
│   ├── boundary_density_estimator.py
│   ├── boundary_entropy_monitor.py
│   ├── boundary_gain_estimator.py
│   ├── boundary_hotspot_tracker.py
│   ├── boundary_refinement_sampler.py
│   ├── boundary_resampling_controller.py
│   ├── boundary_uncertainty_estimator.py
│   ├── boundary_zoom_sampler.py
│   ├── campaign_claim_linter.py
│   ├── campaign_merge_validator.py
│   ├── campaign_outcome_classifier.py
│   ├── campaign_readiness_reporter.py
│   ├── campaign_registry_builder.py
│   ├── campaign_seed_bookkeeper.py
│   ├── candidate_pruning_engine.py
│   ├── causal_graph_discovery.py
│   ├── claim_boundary_reporter.py
│   ├── claim_traceability_builder.py
│   ├── collapse_boundary_curvature_estimator.py
│   ├── collapse_phase_transition_mapper.py
│   ├── collapse_surface_mapper.py
│   ├── collapse_surface_visualizer.py
│   ├── confidence_interval_engine.py
│   ├── confidence_interval_mapper.py
│   ├── control_law_synthesizer.py
│   ├── cosmology_invariant_tester.py
│   ├── cosmology_quantum_convergence_tester.py
│   ├── critical_band_sampler.py
│   ├── critical_surface_confidence_map.py
│   ├── critical_surface_mapper.py
│   ├── critical_threshold_fitter.py
│   ├── cross_baseline_comparator.py
│   ├── cross_campaign_comparator.py
│   ├── cross_dataset_consistency_checker.py
│   ├── cross_domain_disagreement_detector.py
│   ├── cross_domain_invariant_comparator.py
│   ├── cross_domain_invariant_tester.py
│   ├── cross_domain_invariant_validator.py
│   ├── cross_domain_mapping_engine.py
│   ├── cross_domain_remapping_runner.py
│   ├── cross_domain_validation_manifest.py
│   ├── cross_federation_baseline_comparator.py
│   ├── cross_node_uc_aggregator.py
│   ├── cross_sandbox_replication_runner.py
│   ├── cross_scale_comparator.py
│   ├── cross_scale_invariant_checker.py
│   ├── cross_scale_replication_runner.py
│   ├── cross_scale_uc_comparator.py
│   ├── cross_scale_validation_engine.py
│   ├── deterministic_seed_controller.py
│   ├── dimensionless_ratio_detector.py
│   ├── discovery_confidence_aggregator.py
│   ├── discovery_convergence_tracker.py
│   ├── discovery_cycle_forecaster.py
│   ├── discovery_cycle_orchestrator.py
│   ├── discovery_energy_optimizer.py
│   ├── discovery_entropy_analyzer.py
│   ├── discovery_explanation_generator.py
│   ├── discovery_feedback_controller.py
│   ├── discovery_graph_engine.py
│   ├── discovery_graph_visualizer.py
│   ├── discovery_novelty_engine.py
│   ├── discovery_priority_scheduler.py
│   ├── discovery_signal_filter.py
│   ├── discovery_signal_ranker.py
│   ├── discovery_timeline_builder.py
│   ├── discovery_uncertainty_tracker.py
│   ├── distributed_claim_evaluator.py
│   ├── distributed_confidence_synthesizer.py
│   ├── distributed_research_marketplace.py
│   ├── distributed_sandbox_router.py
│   ├── distributed_theorem_candidate_registry.py
│   ├── domain_adaptation_queue_builder.py
│   ├── domain_transfer_scorecard.py
│   ├── event_stream.py
│   ├── evolutionary_invariant_search.py
│   ├── experiment_hash_verifier.py
│   ├── experiment_quota_manager.py
│   ├── experiment_registry.json
│   ├── experiment_replay_runner.py
│   ├── experiment_run_registry.py
│   ├── experiment_scheduler_cluster.py
│   ├── experiment_space_mapper.py
│   ├── exponent_stability_tracker.py
│   ├── falsification_tournament_engine.py
│   ├── federated_consensus_notary.py
│   ├── federated_experiment_router.py
│   ├── federated_node_auth_registry.py
│   ├── federated_receipt_verifier.py
│   ├── federated_result_merger.py
│   ├── federated_result_validator.py
│   ├── federation_latency_tracker.py
│   ├── fixed_point_detector.py
│   ├── gcat_atlas_finalizer.py
│   ├── global_experiment_index.py
│   ├── global_gcat_atlas_builder.py
│   ├── global_invariant_registry.py
│   ├── global_invariant_scoreboard.py
│   ├── global_phase_space_aggregator.py
│   ├── global_result_normalizer.py
│   ├── global_stability_atlas_builder.py
│   ├── high_value_region_registry.py
│   ├── hypothesis_mutation_engine.py
│   ├── hypothesis_ranking_engine.py
│   ├── information_gain_ranker.py
│   ├── invariant_atlas_expander.py
│   ├── invariant_candidate_ranker.py
│   ├── invariant_candidate_registry.py
│   ├── invariant_competition_engine.py
│   ├── invariant_competition_leaderboard.py
│   ├── invariant_confidence_estimator.py
│   ├── invariant_confidence_tracker.py
│   ├── invariant_conflict_detector.py
│   ├── invariant_counterexample_finder.py
│   ├── invariant_drift_detector.py
│   ├── invariant_generalization_engine.py
│   ├── invariant_pressure_analyzer.py
│   ├── invariant_result_summary_builder.py
│   ├── invariant_significance_test.py
│   ├── invariant_stability_analyzer.py
│   ├── invariant_stability_tester.py
│   ├── invariant_stress_tester.py
│   ├── large_scale_monte_carlo_engine.py
│   ├── live_dashboard.py
│   ├── merge_diagnostics_reporter.py
│   ├── meta_experiment_planner.py
│   ├── meta_theory_builder.py
│   ├── multi_dataset_invariant_validator.py
│   ├── multi_domain_scaling_analyzer.py
│   ├── multi_lab_readiness_gate.py
│   ├── multi_run_uc_aggregator.py
│   ├── multi_sandbox_consistency_checker.py
│   ├── multi_scale_phase_mapper.py
│   ├── multi_scale_uc_estimator.py
│   ├── next_experiment_selector.py
│   ├── paper_generation_engine.py
│   ├── parallel_shard_metadata_writer.py
│   ├── parameter_sensitivity_analyzer.py
│   ├── peer_disagreement_analyzer.py
│   ├── peer_invariant_agreement_scorer.py
│   ├── phase_animation.py
│   ├── phase_boundary_density_map.py
│   ├── phase_boundary_tracker.py
│   ├── phase_space_heatmap_generator.py
│   ├── publication_bundle_builder.py
│   ├── publication_readiness_gate.py
│   ├── quantum_invariant_tester.py
│   ├── README.md
│   ├── renormalization_group_scaler.py
│   ├── replay_engine.py
│   ├── replication_success_dashboard.py
│   ├── replication_success_tracker.py
│   ├── reproducibility_audit_engine.py
│   ├── reproducibility_scorecard.py
│   ├── research_autopilot.py
│   ├── research_campaign_summary_builder.py
│   ├── research_graph_optimizer.py
│   ├── research_integrity_checker.py
│   ├── research_lineage_tracker.py
│   ├── research_module_226.py
│   ├── research_module_227.py
│   ├── research_module_228.py
│   ├── research_module_229.py
│   ├── research_module_230.py
│   ├── research_module_231.py
│   ├── research_module_232.py
│   ├── research_module_233.py
│   ├── research_module_234.py
│   ├── research_module_235.py
│   ├── research_module_236.py
│   ├── research_module_237.py
│   └── research_module_238.py
├── path-safety-upgrade-bundle
│   ├── ingestion
│   │   ├── ingest_bundle_safe.py
│   │   └── path_safety.py
│   └── README.md
├── payload
│   ├── actuation
│   │   ├── 0001_bundle_version____1_0____review_purpose____sdk_review_and_external_packaging.json
│   │   ├── 0002_claims____proven_by_demo___the_critical_ratio_campaign_computes_the_candidate.json
│   │   ├── 0003_claims____proven_by_demo___the_experiment_computes_the_candidate_invariant_u_e.json
│   │   ├── 0004_the_critical_ratio_campaign_computes_the_candidate_invariant__u__as_specified.json
│   │   ├── 0005_the_experiment_computes_the_candidate_invariant_u_exactly_as_specified.json
│   │   ├── 0006_the_candidate_invariant_can_be_compared_against_simpler_baseline_ratios.json
│   │   ├── 0007_supported_by_demo___the_candidate_invariant_can_be_compared_against_simpler_b.json
│   │   ├── 0008_the_validation_scripts_can_check_deterministic_and_statistical_output_artifacts.json
│   │   ├── 0009_the_validation_scripts_can_check_deterministic_and_statistical_output_artifact.json
│   │   ├── 0010_bundle_version____1_0____review_purpose____sdk_review_and_external_packaging.json
│   │   └── actuation_summary.md
│   ├── anomaly_detection
│   │   ├── anomaly_report.json
│   │   └── anomaly_report.md
│   ├── autonomy_plane
│   │   ├── adaptive_boundary_targeter.py
│   │   ├── adaptive_shard_reweighting_engine.py
│   │   ├── autonomous_baseline_builder.py
│   │   ├── autonomous_summary_notary.py
│   │   ├── autonomy_safety_gate.py
│   │   ├── boundary_focus_controller.py
│   │   ├── candidate_law_compactor.py
│   │   ├── candidate_law_promotion_gate.py
│   │   ├── convergence_certificate_builder.py
│   │   ├── convergence_stop_recommender.py
│   │   ├── counterexample_hunter.py
│   │   ├── critical_region_queue.py
│   │   ├── cross_scale_target_allocator.py
│   │   ├── disagreement_retest_scheduler.py
│   │   ├── discovery_receipt_writer.py
│   │   ├── experiment_retry_policy_builder.py
│   │   ├── experiment_space_pruner.py
│   │   ├── exploration_reward_model.py
│   │   ├── followup_run_recommender.py
│   │   ├── global_boundary_snapshotter.py
│   │   ├── law_stability_dashboard.py
│   │   ├── meta_hypothesis_ranker.py
│   │   ├── phase_transition_scorecard.py
│   │   ├── regime_shift_alert_engine.py
│   │   ├── replication_priority_router.py
│   │   ├── research_checkpoint_writer.py
│   │   ├── research_goal_router.py
│   │   ├── result_salience_estimator.py
│   │   ├── theorem_refinement_loop.py
│   │   └── uncertainty_gradient_mapper.py
│   ├── canonical
│   │   └── run_eval.py
│   ├── canonical_repo
│   │   ├── .github
│   │   │   └── workflows
│   │   │       └── forced_ingest_and_eval.yml
│   │   ├── adaptive_v20
│   │   │   ├── .github
│   │   │   │   └── workflows
│   │   │   │       └── run.yml
│   │   │   ├── config
│   │   │   │   └── policy.json
│   │   │   └── experiments
│   │   │       └── evaluation_suite
│   │   │           └── run_eval.py
│   │   ├── config
│   │   │   └── policy.json
│   │   ├── experiments
│   │   │   └── evaluation_suite
│   │   │       └── run_eval.py
│   │   └── install
│   │       ├── bcat_engine.py
│   │       ├── consensus_engine.py
│   │       ├── crypto_keys.py
│   │       ├── network_registry.py
│   │       ├── policy_engine.py
│   │       └── receipt_guard.py
│   ├── cluster_plane
│   │   ├── campaign_retry_controller.py
│   │   ├── cluster_artifact_cache.py
│   │   ├── cluster_execution_manifest.json
│   │   ├── compute_budget_allocator.py
│   │   ├── cross_cluster_merge_coordinator.py
│   │   ├── distributed_run_manifest_builder.py
│   │   ├── distributed_seed_namespace.py
│   │   ├── distributed_shard_scheduler.py
│   │   ├── result_shard_consolidator.py
│   │   ├── worker_capacity_registry.py
│   │   └── worker_failure_recovery_stub.py
│   ├── config
│   │   ├── eval_config.json
│   │   └── v8_policy.json
│   ├── control_plane
│   │   ├── tc
│   │   │   ├── bundle_install.tc.json
│   │   │   └── README.md
│   │   ├── tvc
│   │   │   ├── README.md
│   │   │   └── verify_bundle_install.py
│   │   ├── .gitkeep
│   │   ├── override.json
│   │   └── README.md
│   ├── discovery_engine
│   │   ├── adaptive_campaign_auditor.py
│   │   ├── adaptive_information_budgeter.py
│   │   ├── boundary_shape_classifier.py
│   │   ├── campaign_auto_stop_detector.py
│   │   ├── critical_band_navigator.py
│   │   ├── critical_ratio_competitor_search.py
│   │   ├── cross_dataset_novelty_monitor.py
│   │   ├── cross_domain_transfer_planner.py
│   │   ├── evidence_density_tracker.py
│   │   ├── experiment_termination_policy.py
│   │   ├── followup_campaign_generator.py
│   │   ├── high_value_boundary_sampler.py
│   │   ├── invariant_retention_scheduler.py
│   │   ├── novelty_score_estimator.py
│   │   ├── symbolic_regression_stub.py
│   │   └── transition_regime_labeler.py
│   ├── docs
│   │   ├── architecture
│   │   │   ├── ARCHITECTURE_DIAGRAM.md
│   │   │   └── PROPOSED_BUILD.md
│   │   ├── demo_suite_suggestions
│   │   │   └── critical_ratio_campaign
│   │   │       ├── baselines.py
│   │   │       ├── CLAIMS.md
│   │   │       ├── expected_outputs.json
│   │   │       ├── experiment_config.json
│   │   │       ├── falsification_tests.py
│   │   │       ├── protocol.md
│   │   │       ├── README.md
│   │   │       └── validate_results.py
│   │   └── research
│   │       └── RUNTIME_THEORY.md
│   ├── evidence_plane
│   │   ├── ledger
│   │   │   ├── append_ledger.py
│   │   │   ├── merkle_root.py
│   │   │   └── README.md
│   │   ├── replay
│   │   │   ├── README.md
│   │   │   └── replay_receipt.py
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   └── receipt.py
│   ├── execution_plane
│   │   ├── sandbox_runner
│   │   │   └── README.md
│   │   └── README.md
│   ├── experiments
│   │   └── critical_ratio_campaign
│   │       ├── results
│   │       │   └── README.md
│   │       ├── baselines.py
│   │       ├── CLAIMS.md
│   │       ├── expanded_experiment_config.json
│   │       ├── expected_outputs.json
│   │       ├── experiment_config.json
│   │       ├── falsification_tests.py
│   │       ├── protocol.md
│   │       ├── README.md
│   │       ├── run_expanded_experiment.py
│   │       ├── run_experiment.py
│   │       ├── validate_results.py
│   │       └── visualize_phase_space.py
│   ├── federation_plane
│   │   ├── cross_lab_verification_router.py
│   │   ├── cross_node_campaign_dispatcher.py
│   │   ├── dataset_sync_scheduler.py
│   │   ├── distributed_claim_consensus.py
│   │   ├── federation_manifest.json
│   │   ├── federation_node_registry.py
│   │   ├── network_health_broadcaster.py
│   │   ├── peer_receipt_ledger_bridge.py
│   │   ├── peer_result_ingestor.py
│   │   ├── peer_validation_registry.py
│   │   └── remote_artifact_notary.py
│   ├── feedback
│   │   ├── canonical_feedback.json
│   │   ├── canonical_feedback.md
│   │   ├── canonical_loop_report.json
│   │   └── failed_bundle_report_correlation.json
│   ├── fixed_manifests
│   │   ├── publishable_demo_export_bundle_v1.bundle_manifest.json
│   │   ├── sandbox_autonomous_loop_stabilization_v1.bundle_manifest.json
│   │   ├── sandbox_closed_loop_activation_v1.bundle_manifest.json
│   │   ├── sandbox_next_50_upgrades_981_1030_v1.bundle_manifest.json
│   │   └── sandbox_research_grade_upgrades_1031_1040_v1.bundle_manifest.json
│   ├── global_registry
│   │   ├── cross_lab_invariant_index.py
│   │   ├── dataset_provenance_registry.py
│   │   ├── evidence_chain_linker.py
│   │   ├── export_bundle_registry.py
│   │   ├── future_roadmap_783_900.json
│   │   ├── global_confidence_estimator.py
│   │   ├── global_uc_estimate_tracker.py
│   │   ├── invariant_registry_core.py
│   │   ├── invariant_version_tracker.py
│   │   ├── multi_scale_invariant_map.py
│   │   ├── registry_audit_log.py
│   │   ├── run_receipt_registry.py
│   │   └── theorem_candidate_registry.py
│   ├── identity_plane
│   │   ├── artifact_watermark_stub.py
│   │   ├── compute_capacity_exchange.py
│   │   ├── cross_lab_contract_registry.py
│   │   ├── dataset_quality_scoreboard.py
│   │   ├── identity_resolution_api_stub.py
│   │   ├── marketplace_dispute_tracker.py
│   │   ├── marketplace_health_dashboard.py
│   │   ├── peer_reputation_verifier.py
│   │   ├── permissioned_download_gate.py
│   │   ├── research_collaboration_board.py
│   │   └── trust_anchor_manager.py
│   ├── injection
│   │   ├── feedback_policy_inputs.json
│   │   ├── feedback_prompt_inputs.json
│   │   └── feedback_prompt_inputs.md
│   ├── install
│   │   └── README.md
│   ├── knowledge_delta
│   │   ├── knowledge_delta.json
│   │   └── knowledge_delta.md
│   ├── marketplace_plane
│   │   ├── artifact_license_tracker.py
│   │   ├── compute_contributor_registry.py
│   │   ├── compute_offer_matcher.py
│   │   ├── consent_bound_export_gate.py
│   │   ├── contributor_payout_stub.py
│   │   ├── dataset_access_policy_engine.py
│   │   ├── dataset_contributor_registry.py
│   │   ├── dataset_exchange_registry.py
│   │   ├── dataset_usage_meter.py
│   │   ├── experiment_bid_router.py
│   │   ├── experiment_credit_ledger.py
│   │   ├── experiment_patronage_router.py
│   │   ├── grant_tracking_stub.py
│   │   ├── identity_audit_log.py
│   │   ├── marketplace_fee_router.py
│   │   ├── marketplace_listing_builder.py
│   │   ├── node_attestation_registry.py
│   │   ├── node_trust_scorecard.py
│   │   ├── policy_receipt_market_linker.py
│   │   ├── proof_of_replication_stub.py
│   │   ├── public_key_directory.py
│   │   ├── receipt_bound_identity_linker.py
│   │   ├── receipt_signature_exchange.py
│   │   ├── replication_reward_router.py
│   │   ├── researcher_identity_registry.py
│   │   ├── researcher_reputation_index.py
│   │   ├── sponsor_visibility_registry.py
│   │   ├── trust_badge_generator.py
│   │   └── trust_decay_monitor.py
│   ├── network
│   │   └── peers.json
│   ├── observation_plane
│   │   ├── phase_space
│   │   │   └── README.md
│   │   └── README.md
│   ├── observatory
│   │   ├── state_log
│   │   │   ├── record_runtime_event.py
│   │   │   └── record_state.py
│   │   ├── .gitkeep
│   │   ├── adaptive_boundary_discovery_engine.py
│   │   ├── adaptive_campaign_controller.py
│   │   ├── adaptive_campaign_launcher.py
│   │   ├── adaptive_hypothesis_pruner.py
│   │   ├── adaptive_intervention_planner.py
│   │   ├── adaptive_model_refitter.py
│   │   ├── adaptive_rg_refinement.py
│   │   ├── adaptive_sampling_scorecard.py
│   │   ├── adaptive_shard_allocator.py
│   │   ├── adaptive_uc_refiner.py
│   │   ├── anomaly_cluster_detector.py
│   │   ├── anomaly_discovery_engine.py
│   │   ├── anomaly_root_cause_analyzer.py
│   │   ├── automated_dataset_curator.py
│   │   ├── automated_null_hypothesis_tester.py
│   │   ├── automated_research_report_builder.py
│   │   ├── autonomous_campaign_scheduler.py
│   │   ├── autonomous_dataset_refiner.py
│   │   ├── autonomous_experiment_generator.py
│   │   ├── autonomous_research_cycle_manager.py
│   │   ├── autonomous_research_supervisor.py
│   │   ├── autonomous_theorem_publisher.py
│   │   ├── autonomous_theory_director.py
│   │   ├── beta_tracking_engine.py
│   │   ├── bootstrap_validation_engine.py
│   │   ├── boundary_density_estimator.py
│   │   ├── boundary_entropy_monitor.py
│   │   ├── boundary_gain_estimator.py
│   │   ├── boundary_hotspot_tracker.py
│   │   ├── boundary_refinement_sampler.py
│   │   ├── boundary_resampling_controller.py
│   │   ├── boundary_uncertainty_estimator.py
│   │   ├── boundary_zoom_sampler.py
│   │   ├── campaign_claim_linter.py
│   │   ├── campaign_merge_validator.py
│   │   ├── campaign_outcome_classifier.py
│   │   ├── campaign_readiness_reporter.py
│   │   ├── campaign_registry_builder.py
│   │   ├── campaign_seed_bookkeeper.py
│   │   ├── candidate_pruning_engine.py
│   │   ├── causal_graph_discovery.py
│   │   ├── claim_boundary_reporter.py
│   │   ├── claim_traceability_builder.py
│   │   ├── collapse_boundary_curvature_estimator.py
│   │   ├── collapse_phase_transition_mapper.py
│   │   ├── collapse_surface_mapper.py
│   │   ├── collapse_surface_visualizer.py
│   │   ├── confidence_interval_engine.py
│   │   ├── confidence_interval_mapper.py
│   │   ├── control_law_synthesizer.py
│   │   ├── cosmology_invariant_tester.py
│   │   ├── cosmology_quantum_convergence_tester.py
│   │   ├── critical_band_sampler.py
│   │   ├── critical_surface_confidence_map.py
│   │   ├── critical_surface_mapper.py
│   │   ├── critical_threshold_fitter.py
│   │   ├── cross_baseline_comparator.py
│   │   ├── cross_campaign_comparator.py
│   │   ├── cross_dataset_consistency_checker.py
│   │   ├── cross_domain_disagreement_detector.py
│   │   ├── cross_domain_invariant_comparator.py
│   │   ├── cross_domain_invariant_tester.py
│   │   ├── cross_domain_invariant_validator.py
│   │   ├── cross_domain_mapping_engine.py
│   │   ├── cross_domain_remapping_runner.py
│   │   ├── cross_domain_validation_manifest.py
│   │   ├── cross_federation_baseline_comparator.py
│   │   ├── cross_node_uc_aggregator.py
│   │   ├── cross_sandbox_replication_runner.py
│   │   ├── cross_scale_comparator.py
│   │   ├── cross_scale_invariant_checker.py
│   │   ├── cross_scale_replication_runner.py
│   │   ├── cross_scale_uc_comparator.py
│   │   ├── cross_scale_validation_engine.py
│   │   ├── deterministic_seed_controller.py
│   │   ├── dimensionless_ratio_detector.py
│   │   ├── discovery_confidence_aggregator.py
│   │   ├── discovery_convergence_tracker.py
│   │   ├── discovery_cycle_forecaster.py
│   │   ├── discovery_cycle_orchestrator.py
│   │   ├── discovery_energy_optimizer.py
│   │   ├── discovery_entropy_analyzer.py
│   │   ├── discovery_explanation_generator.py
│   │   ├── discovery_feedback_controller.py
│   │   ├── discovery_graph_engine.py
│   │   ├── discovery_graph_visualizer.py
│   │   ├── discovery_novelty_engine.py
│   │   ├── discovery_priority_scheduler.py
│   │   ├── discovery_signal_filter.py
│   │   ├── discovery_signal_ranker.py
│   │   ├── discovery_timeline_builder.py
│   │   ├── discovery_uncertainty_tracker.py
│   │   ├── distributed_claim_evaluator.py
│   │   ├── distributed_confidence_synthesizer.py
│   │   ├── distributed_research_marketplace.py
│   │   ├── distributed_sandbox_router.py
│   │   ├── distributed_theorem_candidate_registry.py
│   │   ├── domain_adaptation_queue_builder.py
│   │   ├── domain_transfer_scorecard.py
│   │   ├── evolutionary_invariant_search.py
│   │   ├── experiment_hash_verifier.py
│   │   ├── experiment_quota_manager.py
│   │   ├── experiment_registry.json
│   │   ├── experiment_replay_runner.py
│   │   ├── experiment_run_registry.py
│   │   ├── experiment_scheduler_cluster.py
│   │   ├── experiment_space_mapper.py
│   │   ├── exponent_stability_tracker.py
│   │   ├── falsification_tournament_engine.py
│   │   ├── federated_consensus_notary.py
│   │   ├── federated_experiment_router.py
│   │   ├── federated_node_auth_registry.py
│   │   ├── federated_receipt_verifier.py
│   │   ├── federated_result_merger.py
│   │   ├── federated_result_validator.py
│   │   ├── federation_latency_tracker.py
│   │   ├── fixed_point_detector.py
│   │   ├── gcat_atlas_finalizer.py
│   │   ├── global_experiment_index.py
│   │   ├── global_gcat_atlas_builder.py
│   │   ├── global_invariant_registry.py
│   │   ├── global_invariant_scoreboard.py
│   │   ├── global_phase_space_aggregator.py
│   │   ├── global_result_normalizer.py
│   │   ├── global_stability_atlas_builder.py
│   │   ├── high_value_region_registry.py
│   │   ├── hypothesis_mutation_engine.py
│   │   ├── hypothesis_ranking_engine.py
│   │   ├── information_gain_ranker.py
│   │   ├── invariant_atlas_expander.py
│   │   ├── invariant_candidate_ranker.py
│   │   ├── invariant_candidate_registry.py
│   │   ├── invariant_competition_engine.py
│   │   ├── invariant_competition_leaderboard.py
│   │   ├── invariant_confidence_estimator.py
│   │   ├── invariant_confidence_tracker.py
│   │   ├── invariant_conflict_detector.py
│   │   ├── invariant_counterexample_finder.py
│   │   ├── invariant_drift_detector.py
│   │   ├── invariant_generalization_engine.py
│   │   ├── invariant_pressure_analyzer.py
│   │   ├── invariant_result_summary_builder.py
│   │   ├── invariant_significance_test.py
│   │   ├── invariant_stability_analyzer.py
│   │   ├── invariant_stability_tester.py
│   │   ├── invariant_stress_tester.py
│   │   ├── large_scale_monte_carlo_engine.py
│   │   ├── merge_diagnostics_reporter.py
│   │   ├── meta_experiment_planner.py
│   │   ├── meta_theory_builder.py
│   │   ├── multi_dataset_invariant_validator.py
│   │   ├── multi_domain_scaling_analyzer.py
│   │   ├── multi_lab_readiness_gate.py
│   │   ├── multi_run_uc_aggregator.py
│   │   ├── multi_sandbox_consistency_checker.py
│   │   ├── multi_scale_phase_mapper.py
│   │   ├── multi_scale_uc_estimator.py
│   │   ├── next_experiment_selector.py
│   │   ├── paper_generation_engine.py
│   │   ├── parallel_shard_metadata_writer.py
│   │   ├── parameter_sensitivity_analyzer.py
│   │   ├── peer_disagreement_analyzer.py
│   │   ├── peer_invariant_agreement_scorer.py
│   │   ├── phase_boundary_density_map.py
│   │   ├── phase_boundary_tracker.py
│   │   ├── phase_space_heatmap_generator.py
│   │   ├── publication_bundle_builder.py
│   │   ├── publication_readiness_gate.py
│   │   ├── quantum_invariant_tester.py
│   │   ├── README.md
│   │   ├── renormalization_group_scaler.py
│   │   ├── replication_success_dashboard.py
│   │   ├── replication_success_tracker.py
│   │   ├── reproducibility_audit_engine.py
│   │   ├── reproducibility_scorecard.py
│   │   ├── research_autopilot.py
│   │   ├── research_campaign_summary_builder.py
│   │   ├── research_graph_optimizer.py
│   │   ├── research_integrity_checker.py
│   │   ├── research_lineage_tracker.py
│   │   ├── research_module_226.py
│   │   ├── research_module_227.py
│   │   ├── research_module_228.py
│   │   ├── research_module_229.py
│   │   ├── research_module_230.py
│   │   ├── research_module_231.py
│   │   ├── research_module_232.py
│   │   ├── research_module_233.py
│   │   ├── research_module_234.py
│   │   ├── research_module_235.py
│   │   ├── research_module_236.py
│   │   ├── research_module_237.py
│   │   ├── research_module_238.py
│   │   ├── research_module_239.py
│   │   ├── research_module_240.py
│   │   ├── research_module_241.py
│   │   ├── research_module_242.py
│   │   └── research_module_243.py
│   ├── publication_plane
│   │   ├── artifact_archive_builder.py
│   │   ├── artifact_bundle_signer.py
│   │   ├── autonomous_publication_gate.py
│   │   ├── citation_trace_exporter.py
│   │   ├── claim_to_figure_linker.py
│   │   ├── dataset_bundle_publisher.py
│   │   ├── dataset_doi_stub.py
│   │   ├── demo_latest_pointer_builder.py
│   │   ├── demo_repo_sync_agent.py
│   │   ├── demo_surface_sync_agent.py
│   │   ├── evidence_appendix_builder.py
│   │   ├── export_demo_pipeline.py
│   │   ├── external_dataset_exporter.py
│   │   ├── figure_manifest_builder.py
│   │   ├── global_registry_sync_agent.py
│   │   ├── merge_summary_publisher.py
│   │   ├── methodology_packet_exporter.py
│   │   ├── open_data_catalog_updater.py
│   │   ├── open_review_packet_builder.py
│   │   ├── paper_outline_synthesizer.py
│   │   ├── press_summary_generator.py
│   │   ├── public_dashboard_snapshotter.py
│   │   ├── public_summary_page_builder.py
│   │   ├── publication_health_monitor.py
│   │   ├── publication_receipt_writer.py
│   │   ├── publication_summary_builder.py
│   │   ├── publish_demo_surface.py
│   │   ├── release_channel_router.py
│   │   ├── replication_badge_generator.py
│   │   ├── replication_badge_publisher.py
│   │   ├── research_publication_router.py
│   │   ├── research_release_manager.py
│   │   ├── research_release_notary.py
│   │   ├── result_snapshot_builder.py
│   │   ├── results_readme_refresher.py
│   │   ├── review_round_tracker.py
│   │   ├── summary_card_builder.py
│   │   ├── table_packager.py
│   │   └── user_facing_result_packet_builder.py
│   ├── receipts
│   │   ├── actuator_bridge
│   │   │   ├── actuator_bridge_0001.json
│   │   │   ├── actuator_bridge_0002.json
│   │   │   ├── actuator_bridge_0003.json
│   │   │   ├── actuator_bridge_0004.json
│   │   │   ├── actuator_bridge_0005.json
│   │   │   ├── actuator_bridge_0006.json
│   │   │   ├── actuator_bridge_0007.json
│   │   │   ├── actuator_bridge_0008.json
│   │   │   ├── actuator_bridge_0009.json
│   │   │   ├── actuator_bridge_0010.json
│   │   │   ├── actuator_bridge_0011.json
│   │   │   ├── actuator_bridge_0012.json
│   │   │   ├── actuator_bridge_0013.json
│   │   │   ├── actuator_bridge_0014.json
│   │   │   ├── actuator_bridge_0015.json
│   │   │   ├── actuator_bridge_0016.json
│   │   │   ├── actuator_bridge_0017.json
│   │   │   ├── actuator_bridge_0018.json
│   │   │   ├── actuator_bridge_0019.json
│   │   │   ├── actuator_bridge_0020.json
│   │   │   ├── actuator_bridge_0021.json
│   │   │   ├── actuator_bridge_0022.json
│   │   │   ├── actuator_bridge_0023.json
│   │   │   ├── actuator_bridge_0024.json
│   │   │   ├── actuator_bridge_0025.json
│   │   │   ├── actuator_bridge_0026.json
│   │   │   ├── actuator_bridge_0027.json
│   │   │   ├── actuator_bridge_0028.json
│   │   │   ├── actuator_bridge_0029.json
│   │   │   ├── actuator_bridge_0030.json
│   │   │   ├── actuator_bridge_0031.json
│   │   │   ├── actuator_bridge_0032.json
│   │   │   ├── actuator_bridge_0033.json
│   │   │   ├── actuator_bridge_0034.json
│   │   │   ├── actuator_bridge_0035.json
│   │   │   ├── actuator_bridge_0036.json
│   │   │   ├── actuator_bridge_0037.json
│   │   │   ├── actuator_bridge_0038.json
│   │   │   ├── actuator_bridge_0039.json
│   │   │   ├── actuator_bridge_0040.json
│   │   │   ├── actuator_bridge_0041.json
│   │   │   ├── actuator_bridge_0042.json
│   │   │   ├── actuator_bridge_0043.json
│   │   │   ├── actuator_bridge_0044.json
│   │   │   ├── actuator_bridge_0045.json
│   │   │   ├── actuator_bridge_0046.json
│   │   │   ├── actuator_bridge_0047.json
│   │   │   ├── actuator_bridge_0048.json
│   │   │   └── actuator_bridge_0049.json
│   │   ├── adaptive_priority
│   │   │   └── adaptive_priority_0001.json
│   │   ├── anomaly_detection
│   │   │   └── anomaly_detection_0001.json
│   │   ├── canonical_feedback
│   │   │   ├── canonical_feedback_0001.json
│   │   │   ├── canonical_feedback_0002.json
│   │   │   ├── canonical_feedback_0003.json
│   │   │   ├── canonical_feedback_0004.json
│   │   │   ├── canonical_feedback_0005.json
│   │   │   ├── canonical_feedback_0006.json
│   │   │   ├── canonical_feedback_0007.json
│   │   │   ├── canonical_feedback_0008.json
│   │   │   ├── canonical_feedback_0009.json
│   │   │   ├── canonical_feedback_0010.json
│   │   │   ├── canonical_feedback_0011.json
│   │   │   ├── canonical_feedback_0012.json
│   │   │   ├── canonical_feedback_0013.json
│   │   │   ├── canonical_feedback_0014.json
│   │   │   ├── canonical_feedback_0015.json
│   │   │   ├── canonical_feedback_0016.json
│   │   │   ├── canonical_feedback_0017.json
│   │   │   ├── canonical_feedback_0018.json
│   │   │   ├── canonical_feedback_0019.json
│   │   │   ├── canonical_feedback_0020.json
│   │   │   ├── canonical_feedback_0021.json
│   │   │   ├── canonical_feedback_0022.json
│   │   │   ├── canonical_feedback_0023.json
│   │   │   ├── canonical_feedback_0024.json
│   │   │   ├── canonical_feedback_0025.json
│   │   │   ├── canonical_feedback_0026.json
│   │   │   ├── canonical_feedback_0027.json
│   │   │   ├── canonical_feedback_0028.json
│   │   │   ├── canonical_feedback_0029.json
│   │   │   ├── canonical_feedback_0030.json
│   │   │   ├── canonical_feedback_0031.json
│   │   │   ├── canonical_feedback_0032.json
│   │   │   ├── canonical_feedback_0033.json
│   │   │   ├── canonical_feedback_0034.json
│   │   │   ├── canonical_feedback_0035.json
│   │   │   ├── canonical_feedback_0036.json
│   │   │   ├── canonical_feedback_0037.json
│   │   │   ├── canonical_feedback_0038.json
│   │   │   ├── canonical_feedback_0039.json
│   │   │   ├── canonical_feedback_0040.json
│   │   │   ├── canonical_feedback_0041.json
│   │   │   ├── canonical_feedback_0042.json
│   │   │   ├── canonical_feedback_0043.json
│   │   │   ├── canonical_feedback_0044.json
│   │   │   ├── canonical_feedback_0045.json
│   │   │   ├── canonical_feedback_0046.json
│   │   │   ├── canonical_feedback_0047.json
│   │   │   ├── canonical_feedback_0048.json
│   │   │   ├── canonical_feedback_0049.json
│   │   │   ├── canonical_feedback_0050.json
│   │   │   ├── canonical_feedback_0051.json
│   │   │   ├── canonical_feedback_0052.json
│   │   │   ├── canonical_feedback_0053.json
│   │   │   ├── canonical_feedback_0054.json
│   │   │   ├── canonical_feedback_0055.json
│   │   │   ├── canonical_feedback_0056.json
│   │   │   ├── canonical_feedback_0057.json
│   │   │   ├── canonical_feedback_0058.json
│   │   │   ├── canonical_feedback_0059.json
│   │   │   ├── canonical_feedback_0060.json
│   │   │   ├── canonical_feedback_0061.json
│   │   │   ├── canonical_feedback_0062.json
│   │   │   ├── canonical_feedback_0063.json
│   │   │   ├── canonical_feedback_0064.json
│   │   │   ├── canonical_feedback_0065.json
│   │   │   ├── canonical_feedback_0066.json
│   │   │   ├── canonical_feedback_0067.json
│   │   │   ├── canonical_feedback_0068.json
│   │   │   ├── canonical_feedback_0069.json
│   │   │   ├── canonical_feedback_0070.json
│   │   │   ├── canonical_feedback_0071.json
│   │   │   ├── canonical_feedback_0072.json
│   │   │   ├── canonical_feedback_0073.json
│   │   │   ├── canonical_feedback_0074.json
│   │   │   ├── canonical_feedback_0075.json
│   │   │   ├── canonical_feedback_0076.json
│   │   │   ├── canonical_feedback_0077.json
│   │   │   ├── canonical_feedback_0078.json
│   │   │   ├── canonical_feedback_0079.json
│   │   │   ├── canonical_feedback_0080.json
│   │   │   ├── canonical_feedback_0081.json
│   │   │   ├── canonical_feedback_0082.json
│   │   │   ├── canonical_feedback_0083.json
│   │   │   ├── canonical_feedback_0084.json
│   │   │   ├── canonical_feedback_0085.json
│   │   │   ├── canonical_feedback_0086.json
│   │   │   ├── canonical_feedback_0087.json
│   │   │   ├── canonical_feedback_0088.json
│   │   │   ├── canonical_feedback_0089.json
│   │   │   ├── canonical_feedback_0090.json
│   │   │   ├── canonical_feedback_0091.json
│   │   │   ├── canonical_feedback_0092.json
│   │   │   ├── canonical_feedback_0093.json
│   │   │   ├── canonical_feedback_0094.json
│   │   │   ├── canonical_feedback_0095.json
│   │   │   ├── canonical_feedback_0096.json
│   │   │   ├── canonical_feedback_0097.json
│   │   │   ├── canonical_feedback_0098.json
│   │   │   ├── canonical_feedback_0099.json
│   │   │   ├── canonical_feedback_0100.json
│   │   │   ├── canonical_feedback_0101.json
│   │   │   ├── canonical_feedback_0102.json
│   │   │   ├── canonical_feedback_0103.json
│   │   │   ├── canonical_feedback_0104.json
│   │   │   ├── canonical_feedback_0105.json
│   │   │   ├── canonical_feedback_0106.json
│   │   │   ├── canonical_feedback_0107.json
│   │   │   ├── canonical_feedback_0108.json
│   │   │   ├── canonical_feedback_0109.json
│   │   │   ├── canonical_feedback_0110.json
│   │   │   ├── canonical_feedback_0111.json
│   │   │   ├── canonical_feedback_0112.json
│   │   │   ├── canonical_feedback_0113.json
│   │   │   ├── canonical_feedback_0114.json
│   │   │   ├── canonical_feedback_0115.json
│   │   │   ├── canonical_feedback_0116.json
│   │   │   ├── canonical_feedback_0117.json
│   │   │   ├── canonical_feedback_0118.json
│   │   │   ├── canonical_feedback_0119.json
│   │   │   ├── canonical_feedback_0120.json
│   │   │   ├── canonical_feedback_0121.json
│   │   │   ├── canonical_feedback_0122.json
│   │   │   ├── canonical_feedback_0123.json
│   │   │   ├── canonical_feedback_0124.json
│   │   │   └── canonical_feedback_0125.json
│   │   ├── canonical_state
│   │   │   ├── canonical_state_0001.json
│   │   │   ├── canonical_state_0002.json
│   │   │   ├── canonical_state_0003.json
│   │   │   ├── canonical_state_0004.json
│   │   │   ├── canonical_state_0005.json
│   │   │   ├── canonical_state_0006.json
│   │   │   ├── canonical_state_0007.json
│   │   │   ├── canonical_state_0008.json
│   │   │   ├── canonical_state_0009.json
│   │   │   ├── canonical_state_0010.json
│   │   │   ├── canonical_state_0011.json
│   │   │   ├── canonical_state_0012.json
│   │   │   ├── canonical_state_0013.json
│   │   │   ├── canonical_state_0014.json
│   │   │   ├── canonical_state_0015.json
│   │   │   ├── canonical_state_0016.json
│   │   │   ├── canonical_state_0017.json
│   │   │   ├── canonical_state_0018.json
│   │   │   ├── canonical_state_0019.json
│   │   │   ├── canonical_state_0020.json
│   │   │   ├── canonical_state_0021.json
│   │   │   ├── canonical_state_0022.json
│   │   │   ├── canonical_state_0023.json
│   │   │   ├── canonical_state_0024.json
│   │   │   ├── canonical_state_0025.json
│   │   │   ├── canonical_state_0026.json
│   │   │   ├── canonical_state_0027.json
│   │   │   ├── canonical_state_0028.json
│   │   │   ├── canonical_state_0029.json
│   │   │   ├── canonical_state_0030.json
│   │   │   ├── canonical_state_0031.json
│   │   │   ├── canonical_state_0032.json
│   │   │   ├── canonical_state_0033.json
│   │   │   ├── canonical_state_0034.json
│   │   │   ├── canonical_state_0035.json
│   │   │   ├── canonical_state_0036.json
│   │   │   ├── canonical_state_0037.json
│   │   │   ├── canonical_state_0038.json
│   │   │   ├── canonical_state_0039.json
│   │   │   ├── canonical_state_0040.json
│   │   │   ├── canonical_state_0041.json
│   │   │   ├── canonical_state_0042.json
│   │   │   ├── canonical_state_0043.json
│   │   │   ├── canonical_state_0044.json
│   │   │   ├── canonical_state_0045.json
│   │   │   ├── canonical_state_0046.json
│   │   │   ├── canonical_state_0047.json
│   │   │   ├── canonical_state_0048.json
│   │   │   ├── canonical_state_0049.json
│   │   │   ├── canonical_state_0050.json
│   │   │   ├── canonical_state_0051.json
│   │   │   ├── canonical_state_0052.json
│   │   │   ├── canonical_state_0053.json
│   │   │   ├── canonical_state_0054.json
│   │   │   ├── canonical_state_0055.json
│   │   │   ├── canonical_state_0056.json
│   │   │   ├── canonical_state_0057.json
│   │   │   ├── canonical_state_0058.json
│   │   │   ├── canonical_state_0059.json
│   │   │   ├── canonical_state_0060.json
│   │   │   ├── canonical_state_0061.json
│   │   │   ├── canonical_state_0062.json
│   │   │   ├── canonical_state_0063.json
│   │   │   ├── canonical_state_0064.json
│   │   │   ├── canonical_state_0065.json
│   │   │   ├── canonical_state_0066.json
│   │   │   ├── canonical_state_0067.json
│   │   │   ├── canonical_state_0068.json
│   │   │   ├── canonical_state_0069.json
│   │   │   ├── canonical_state_0070.json
│   │   │   ├── canonical_state_0071.json
│   │   │   ├── canonical_state_0072.json
│   │   │   ├── canonical_state_0073.json
│   │   │   ├── canonical_state_0074.json
│   │   │   ├── canonical_state_0075.json
│   │   │   ├── canonical_state_0076.json
│   │   │   ├── canonical_state_0077.json
│   │   │   ├── canonical_state_0078.json
│   │   │   ├── canonical_state_0079.json
│   │   │   ├── canonical_state_0080.json
│   │   │   ├── canonical_state_0081.json
│   │   │   ├── canonical_state_0082.json
│   │   │   ├── canonical_state_0083.json
│   │   │   ├── canonical_state_0084.json
│   │   │   ├── canonical_state_0085.json
│   │   │   ├── canonical_state_0086.json
│   │   │   ├── canonical_state_0087.json
│   │   │   ├── canonical_state_0088.json
│   │   │   ├── canonical_state_0089.json
│   │   │   ├── canonical_state_0090.json
│   │   │   ├── canonical_state_0091.json
│   │   │   ├── canonical_state_0092.json
│   │   │   ├── canonical_state_0093.json
│   │   │   ├── canonical_state_0094.json
│   │   │   ├── canonical_state_0095.json
│   │   │   ├── canonical_state_0096.json
│   │   │   ├── canonical_state_0097.json
│   │   │   ├── canonical_state_0098.json
│   │   │   ├── canonical_state_0099.json
│   │   │   ├── canonical_state_0100.json
│   │   │   ├── canonical_state_0101.json
│   │   │   ├── canonical_state_0102.json
│   │   │   ├── canonical_state_0103.json
│   │   │   ├── canonical_state_0104.json
│   │   │   ├── canonical_state_0105.json
│   │   │   ├── canonical_state_0106.json
│   │   │   ├── canonical_state_0107.json
│   │   │   ├── canonical_state_0108.json
│   │   │   ├── canonical_state_0109.json
│   │   │   ├── canonical_state_0110.json
│   │   │   ├── canonical_state_0111.json
│   │   │   ├── canonical_state_0112.json
│   │   │   ├── canonical_state_0113.json
│   │   │   ├── canonical_state_0114.json
│   │   │   ├── canonical_state_0115.json
│   │   │   ├── canonical_state_0116.json
│   │   │   ├── canonical_state_0117.json
│   │   │   ├── canonical_state_0118.json
│   │   │   ├── canonical_state_0119.json
│   │   │   ├── canonical_state_0120.json
│   │   │   ├── canonical_state_0121.json
│   │   │   ├── canonical_state_0122.json
│   │   │   └── canonical_state_0123.json
│   │   ├── distributed_worker
│   │   │   └── distributed_worker_0001.json
│   │   ├── document_compaction
│   │   │   ├── document_compaction_0001.json
│   │   │   ├── document_compaction_0002.json
│   │   │   ├── document_compaction_0003.json
│   │   │   ├── document_compaction_0004.json
│   │   │   ├── document_compaction_0005.json
│   │   │   ├── document_compaction_0006.json
│   │   │   ├── document_compaction_0007.json
│   │   │   ├── document_compaction_0008.json
│   │   │   ├── document_compaction_0009.json
│   │   │   ├── document_compaction_0010.json
│   │   │   ├── document_compaction_0011.json
│   │   │   ├── document_compaction_0012.json
│   │   │   ├── document_compaction_0013.json
│   │   │   ├── document_compaction_0014.json
│   │   │   ├── document_compaction_0015.json
│   │   │   ├── document_compaction_0016.json
│   │   │   ├── document_compaction_0017.json
│   │   │   ├── document_compaction_0018.json
│   │   │   ├── document_compaction_0019.json
│   │   │   ├── document_compaction_0020.json
│   │   │   ├── document_compaction_0021.json
│   │   │   ├── document_compaction_0022.json
│   │   │   ├── document_compaction_0023.json
│   │   │   ├── document_compaction_0024.json
│   │   │   ├── document_compaction_0025.json
│   │   │   ├── document_compaction_0026.json
│   │   │   ├── document_compaction_0027.json
│   │   │   ├── document_compaction_0028.json
│   │   │   ├── document_compaction_0029.json
│   │   │   ├── document_compaction_0030.json
│   │   │   ├── document_compaction_0031.json
│   │   │   ├── document_compaction_0032.json
│   │   │   ├── document_compaction_0033.json
│   │   │   ├── document_compaction_0034.json
│   │   │   ├── document_compaction_0035.json
│   │   │   ├── document_compaction_0036.json
│   │   │   ├── document_compaction_0037.json
│   │   │   ├── document_compaction_0038.json
│   │   │   ├── document_compaction_0039.json
│   │   │   ├── document_compaction_0040.json
│   │   │   ├── document_compaction_0041.json
│   │   │   ├── document_compaction_0042.json
│   │   │   ├── document_compaction_0043.json
│   │   │   ├── document_compaction_0044.json
│   │   │   ├── document_compaction_0045.json
│   │   │   ├── document_compaction_0046.json
│   │   │   ├── document_compaction_0047.json
│   │   │   ├── document_compaction_0048.json
│   │   │   ├── document_compaction_0049.json
│   │   │   ├── document_compaction_0050.json
│   │   │   ├── document_compaction_0051.json
│   │   │   ├── document_compaction_0052.json
│   │   │   ├── document_compaction_0053.json
│   │   │   ├── document_compaction_0054.json
│   │   │   ├── document_compaction_0055.json
│   │   │   ├── document_compaction_0056.json
│   │   │   ├── document_compaction_0057.json
│   │   │   ├── document_compaction_0058.json
│   │   │   ├── document_compaction_0059.json
│   │   │   ├── document_compaction_0060.json
│   │   │   ├── document_compaction_0061.json
│   │   │   ├── document_compaction_0062.json
│   │   │   ├── document_compaction_0063.json
│   │   │   ├── document_compaction_0064.json
│   │   │   ├── document_compaction_0065.json
│   │   │   ├── document_compaction_0066.json
│   │   │   ├── document_compaction_0067.json
│   │   │   ├── document_compaction_0068.json
│   │   │   ├── document_compaction_0069.json
│   │   │   ├── document_compaction_0070.json
│   │   │   ├── document_compaction_0071.json
│   │   │   ├── document_compaction_0072.json
│   │   │   ├── document_compaction_0073.json
│   │   │   ├── document_compaction_0074.json
│   │   │   ├── document_compaction_0075.json
│   │   │   ├── document_compaction_0076.json
│   │   │   ├── document_compaction_0077.json
│   │   │   ├── document_compaction_0078.json
│   │   │   ├── document_compaction_0079.json
│   │   │   ├── document_compaction_0080.json
│   │   │   ├── document_compaction_0081.json
│   │   │   ├── document_compaction_0082.json
│   │   │   ├── document_compaction_0083.json
│   │   │   ├── document_compaction_0084.json
│   │   │   ├── document_compaction_0085.json
│   │   │   ├── document_compaction_0086.json
│   │   │   ├── document_compaction_0087.json
│   │   │   ├── document_compaction_0088.json
│   │   │   ├── document_compaction_0089.json
│   │   │   ├── document_compaction_0090.json
│   │   │   ├── document_compaction_0091.json
│   │   │   ├── document_compaction_0092.json
│   │   │   ├── document_compaction_0093.json
│   │   │   ├── document_compaction_0094.json
│   │   │   ├── document_compaction_0095.json
│   │   │   ├── document_compaction_0096.json
│   │   │   ├── document_compaction_0097.json
│   │   │   ├── document_compaction_0098.json
│   │   │   ├── document_compaction_0099.json
│   │   │   ├── document_compaction_0100.json
│   │   │   ├── document_compaction_0101.json
│   │   │   ├── document_compaction_0102.json
│   │   │   ├── document_compaction_0103.json
│   │   │   ├── document_compaction_0104.json
│   │   │   ├── document_compaction_0105.json
│   │   │   ├── document_compaction_0106.json
│   │   │   ├── document_compaction_0107.json
│   │   │   ├── document_compaction_0108.json
│   │   │   ├── document_compaction_0109.json
│   │   │   ├── document_compaction_0110.json
│   │   │   ├── document_compaction_0111.json
│   │   │   ├── document_compaction_0112.json
│   │   │   ├── document_compaction_0113.json
│   │   │   ├── document_compaction_0114.json
│   │   │   ├── document_compaction_0115.json
│   │   │   ├── document_compaction_0116.json
│   │   │   ├── document_compaction_0117.json
│   │   │   ├── document_compaction_0118.json
│   │   │   ├── document_compaction_0119.json
│   │   │   ├── document_compaction_0120.json
│   │   │   ├── document_compaction_0121.json
│   │   │   ├── document_compaction_0122.json
│   │   │   ├── document_compaction_0123.json
│   │   │   ├── document_compaction_0124.json
│   │   │   └── document_compaction_0125.json
│   │   ├── failure_recovery
│   │   │   ├── failure_recovery_0001.json
│   │   │   ├── failure_recovery_0002.json
│   │   │   ├── failure_recovery_0003.json
│   │   │   ├── failure_recovery_0004.json
│   │   │   ├── failure_recovery_0005.json
│   │   │   ├── failure_recovery_0006.json
│   │   │   ├── failure_recovery_0007.json
│   │   │   ├── failure_recovery_0008.json
│   │   │   ├── failure_recovery_0009.json
│   │   │   ├── failure_recovery_0010.json
│   │   │   ├── failure_recovery_0011.json
│   │   │   ├── failure_recovery_0012.json
│   │   │   ├── failure_recovery_0013.json
│   │   │   ├── failure_recovery_0014.json
│   │   │   ├── failure_recovery_0015.json
│   │   │   ├── failure_recovery_0016.json
│   │   │   ├── failure_recovery_0017.json
│   │   │   ├── failure_recovery_0018.json
│   │   │   ├── failure_recovery_0019.json
│   │   │   ├── failure_recovery_0020.json
│   │   │   ├── failure_recovery_0021.json
│   │   │   ├── failure_recovery_0022.json
│   │   │   ├── failure_recovery_0023.json
│   │   │   ├── failure_recovery_0024.json
│   │   │   ├── failure_recovery_0025.json
│   │   │   ├── failure_recovery_0026.json
│   │   │   ├── failure_recovery_0027.json
│   │   │   ├── failure_recovery_0028.json
│   │   │   ├── failure_recovery_0029.json
│   │   │   ├── failure_recovery_0030.json
│   │   │   ├── failure_recovery_0031.json
│   │   │   ├── failure_recovery_0032.json
│   │   │   ├── failure_recovery_0033.json
│   │   │   ├── failure_recovery_0034.json
│   │   │   ├── failure_recovery_0035.json
│   │   │   ├── failure_recovery_0036.json
│   │   │   ├── failure_recovery_0037.json
│   │   │   ├── failure_recovery_0038.json
│   │   │   ├── failure_recovery_0039.json
│   │   │   ├── failure_recovery_0040.json
│   │   │   ├── failure_recovery_0041.json
│   │   │   ├── failure_recovery_0042.json
│   │   │   ├── failure_recovery_0043.json
│   │   │   ├── failure_recovery_0044.json
│   │   │   ├── failure_recovery_0045.json
│   │   │   ├── failure_recovery_0046.json
│   │   │   ├── failure_recovery_0047.json
│   │   │   └── failure_recovery_0048.json
│   │   ├── feedback_execution_bridge
│   │   │   ├── feedback_execution_bridge_0001.json
│   │   │   ├── feedback_execution_bridge_0002.json
│   │   │   ├── feedback_execution_bridge_0003.json
│   │   │   ├── feedback_execution_bridge_0004.json
│   │   │   ├── feedback_execution_bridge_0005.json
│   │   │   ├── feedback_execution_bridge_0006.json
│   │   │   ├── feedback_execution_bridge_0007.json
│   │   │   ├── feedback_execution_bridge_0008.json
│   │   │   ├── feedback_execution_bridge_0009.json
│   │   │   ├── feedback_execution_bridge_0010.json
│   │   │   ├── feedback_execution_bridge_0011.json
│   │   │   ├── feedback_execution_bridge_0012.json
│   │   │   ├── feedback_execution_bridge_0013.json
│   │   │   ├── feedback_execution_bridge_0014.json
│   │   │   ├── feedback_execution_bridge_0015.json
│   │   │   ├── feedback_execution_bridge_0016.json
│   │   │   ├── feedback_execution_bridge_0017.json
│   │   │   ├── feedback_execution_bridge_0018.json
│   │   │   ├── feedback_execution_bridge_0019.json
│   │   │   ├── feedback_execution_bridge_0020.json
│   │   │   ├── feedback_execution_bridge_0021.json
│   │   │   ├── feedback_execution_bridge_0022.json
│   │   │   ├── feedback_execution_bridge_0023.json
│   │   │   ├── feedback_execution_bridge_0024.json
│   │   │   ├── feedback_execution_bridge_0025.json
│   │   │   ├── feedback_execution_bridge_0026.json
│   │   │   ├── feedback_execution_bridge_0027.json
│   │   │   ├── feedback_execution_bridge_0028.json
│   │   │   ├── feedback_execution_bridge_0029.json
│   │   │   ├── feedback_execution_bridge_0030.json
│   │   │   ├── feedback_execution_bridge_0031.json
│   │   │   ├── feedback_execution_bridge_0032.json
│   │   │   ├── feedback_execution_bridge_0033.json
│   │   │   ├── feedback_execution_bridge_0034.json
│   │   │   ├── feedback_execution_bridge_0035.json
│   │   │   ├── feedback_execution_bridge_0036.json
│   │   │   ├── feedback_execution_bridge_0037.json
│   │   │   ├── feedback_execution_bridge_0038.json
│   │   │   ├── feedback_execution_bridge_0039.json
│   │   │   ├── feedback_execution_bridge_0040.json
│   │   │   ├── feedback_execution_bridge_0041.json
│   │   │   ├── feedback_execution_bridge_0042.json
│   │   │   ├── feedback_execution_bridge_0043.json
│   │   │   ├── feedback_execution_bridge_0044.json
│   │   │   ├── feedback_execution_bridge_0045.json
│   │   │   ├── feedback_execution_bridge_0046.json
│   │   │   ├── feedback_execution_bridge_0047.json
│   │   │   ├── feedback_execution_bridge_0048.json
│   │   │   ├── feedback_execution_bridge_0049.json
│   │   │   ├── feedback_execution_bridge_0050.json
│   │   │   ├── feedback_execution_bridge_0051.json
│   │   │   ├── feedback_execution_bridge_0052.json
│   │   │   ├── feedback_execution_bridge_0053.json
│   │   │   ├── feedback_execution_bridge_0054.json
│   │   │   ├── feedback_execution_bridge_0055.json
│   │   │   ├── feedback_execution_bridge_0056.json
│   │   │   ├── feedback_execution_bridge_0057.json
│   │   │   ├── feedback_execution_bridge_0058.json
│   │   │   ├── feedback_execution_bridge_0059.json
│   │   │   ├── feedback_execution_bridge_0060.json
│   │   │   ├── feedback_execution_bridge_0061.json
│   │   │   ├── feedback_execution_bridge_0062.json
│   │   │   ├── feedback_execution_bridge_0063.json
│   │   │   ├── feedback_execution_bridge_0064.json
│   │   │   ├── feedback_execution_bridge_0065.json
│   │   │   ├── feedback_execution_bridge_0066.json
│   │   │   ├── feedback_execution_bridge_0067.json
│   │   │   ├── feedback_execution_bridge_0068.json
│   │   │   ├── feedback_execution_bridge_0069.json
│   │   │   ├── feedback_execution_bridge_0070.json
│   │   │   ├── feedback_execution_bridge_0071.json
│   │   │   ├── feedback_execution_bridge_0072.json
│   │   │   ├── feedback_execution_bridge_0073.json
│   │   │   ├── feedback_execution_bridge_0074.json
│   │   │   ├── feedback_execution_bridge_0075.json
│   │   │   ├── feedback_execution_bridge_0076.json
│   │   │   ├── feedback_execution_bridge_0077.json
│   │   │   ├── feedback_execution_bridge_0078.json
│   │   │   ├── feedback_execution_bridge_0079.json
│   │   │   ├── feedback_execution_bridge_0080.json
│   │   │   ├── feedback_execution_bridge_0081.json
│   │   │   ├── feedback_execution_bridge_0082.json
│   │   │   ├── feedback_execution_bridge_0083.json
│   │   │   ├── feedback_execution_bridge_0084.json
│   │   │   ├── feedback_execution_bridge_0085.json
│   │   │   ├── feedback_execution_bridge_0086.json
│   │   │   ├── feedback_execution_bridge_0087.json
│   │   │   ├── feedback_execution_bridge_0088.json
│   │   │   ├── feedback_execution_bridge_0089.json
│   │   │   ├── feedback_execution_bridge_0090.json
│   │   │   ├── feedback_execution_bridge_0091.json
│   │   │   ├── feedback_execution_bridge_0092.json
│   │   │   ├── feedback_execution_bridge_0093.json
│   │   │   ├── feedback_execution_bridge_0094.json
│   │   │   ├── feedback_execution_bridge_0095.json
│   │   │   ├── feedback_execution_bridge_0096.json
│   │   │   ├── feedback_execution_bridge_0097.json
│   │   │   ├── feedback_execution_bridge_0098.json
│   │   │   ├── feedback_execution_bridge_0099.json
│   │   │   ├── feedback_execution_bridge_0100.json
│   │   │   ├── feedback_execution_bridge_0101.json
│   │   │   ├── feedback_execution_bridge_0102.json
│   │   │   ├── feedback_execution_bridge_0103.json
│   │   │   ├── feedback_execution_bridge_0104.json
│   │   │   ├── feedback_execution_bridge_0105.json
│   │   │   ├── feedback_execution_bridge_0106.json
│   │   │   ├── feedback_execution_bridge_0107.json
│   │   │   ├── feedback_execution_bridge_0108.json
│   │   │   ├── feedback_execution_bridge_0109.json
│   │   │   ├── feedback_execution_bridge_0110.json
│   │   │   ├── feedback_execution_bridge_0111.json
│   │   │   ├── feedback_execution_bridge_0112.json
│   │   │   ├── feedback_execution_bridge_0113.json
│   │   │   ├── feedback_execution_bridge_0114.json
│   │   │   ├── feedback_execution_bridge_0115.json
│   │   │   ├── feedback_execution_bridge_0116.json
│   │   │   ├── feedback_execution_bridge_0117.json
│   │   │   ├── feedback_execution_bridge_0118.json
│   │   │   ├── feedback_execution_bridge_0119.json
│   │   │   ├── feedback_execution_bridge_0120.json
│   │   │   ├── feedback_execution_bridge_0121.json
│   │   │   ├── feedback_execution_bridge_0122.json
│   │   │   └── feedback_execution_bridge_0123.json
│   │   ├── feedback_injection
│   │   │   ├── feedback_injection_0001.json
│   │   │   ├── feedback_injection_0002.json
│   │   │   ├── feedback_injection_0003.json
│   │   │   ├── feedback_injection_0004.json
│   │   │   ├── feedback_injection_0005.json
│   │   │   ├── feedback_injection_0006.json
│   │   │   ├── feedback_injection_0007.json
│   │   │   ├── feedback_injection_0008.json
│   │   │   ├── feedback_injection_0009.json
│   │   │   ├── feedback_injection_0010.json
│   │   │   ├── feedback_injection_0011.json
│   │   │   ├── feedback_injection_0012.json
│   │   │   ├── feedback_injection_0013.json
│   │   │   ├── feedback_injection_0014.json
│   │   │   ├── feedback_injection_0015.json
│   │   │   ├── feedback_injection_0016.json
│   │   │   ├── feedback_injection_0017.json
│   │   │   ├── feedback_injection_0018.json
│   │   │   ├── feedback_injection_0019.json
│   │   │   ├── feedback_injection_0020.json
│   │   │   ├── feedback_injection_0021.json
│   │   │   ├── feedback_injection_0022.json
│   │   │   ├── feedback_injection_0023.json
│   │   │   ├── feedback_injection_0024.json
│   │   │   ├── feedback_injection_0025.json
│   │   │   ├── feedback_injection_0026.json
│   │   │   ├── feedback_injection_0027.json
│   │   │   ├── feedback_injection_0028.json
│   │   │   ├── feedback_injection_0029.json
│   │   │   ├── feedback_injection_0030.json
│   │   │   ├── feedback_injection_0031.json
│   │   │   ├── feedback_injection_0032.json
│   │   │   ├── feedback_injection_0033.json
│   │   │   ├── feedback_injection_0034.json
│   │   │   ├── feedback_injection_0035.json
│   │   │   ├── feedback_injection_0036.json
│   │   │   ├── feedback_injection_0037.json
│   │   │   ├── feedback_injection_0038.json
│   │   │   ├── feedback_injection_0039.json
│   │   │   ├── feedback_injection_0040.json
│   │   │   ├── feedback_injection_0041.json
│   │   │   ├── feedback_injection_0042.json
│   │   │   ├── feedback_injection_0043.json
│   │   │   ├── feedback_injection_0044.json
│   │   │   ├── feedback_injection_0045.json
│   │   │   ├── feedback_injection_0046.json
│   │   │   ├── feedback_injection_0047.json
│   │   │   ├── feedback_injection_0048.json
│   │   │   ├── feedback_injection_0049.json
│   │   │   ├── feedback_injection_0050.json
│   │   │   ├── feedback_injection_0051.json
│   │   │   ├── feedback_injection_0052.json
│   │   │   ├── feedback_injection_0053.json
│   │   │   ├── feedback_injection_0054.json
│   │   │   ├── feedback_injection_0055.json
│   │   │   ├── feedback_injection_0056.json
│   │   │   ├── feedback_injection_0057.json
│   │   │   ├── feedback_injection_0058.json
│   │   │   ├── feedback_injection_0059.json
│   │   │   ├── feedback_injection_0060.json
│   │   │   ├── feedback_injection_0061.json
│   │   │   ├── feedback_injection_0062.json
│   │   │   ├── feedback_injection_0063.json
│   │   │   ├── feedback_injection_0064.json
│   │   │   ├── feedback_injection_0065.json
│   │   │   ├── feedback_injection_0066.json
│   │   │   ├── feedback_injection_0067.json
│   │   │   ├── feedback_injection_0068.json
│   │   │   ├── feedback_injection_0069.json
│   │   │   ├── feedback_injection_0070.json
│   │   │   ├── feedback_injection_0071.json
│   │   │   ├── feedback_injection_0072.json
│   │   │   ├── feedback_injection_0073.json
│   │   │   ├── feedback_injection_0074.json
│   │   │   ├── feedback_injection_0075.json
│   │   │   ├── feedback_injection_0076.json
│   │   │   ├── feedback_injection_0077.json
│   │   │   ├── feedback_injection_0078.json
│   │   │   ├── feedback_injection_0079.json
│   │   │   ├── feedback_injection_0080.json
│   │   │   ├── feedback_injection_0081.json
│   │   │   ├── feedback_injection_0082.json
│   │   │   ├── feedback_injection_0083.json
│   │   │   ├── feedback_injection_0084.json
│   │   │   ├── feedback_injection_0085.json
│   │   │   ├── feedback_injection_0086.json
│   │   │   ├── feedback_injection_0087.json
│   │   │   ├── feedback_injection_0088.json
│   │   │   ├── feedback_injection_0089.json
│   │   │   ├── feedback_injection_0090.json
│   │   │   ├── feedback_injection_0091.json
│   │   │   ├── feedback_injection_0092.json
│   │   │   ├── feedback_injection_0093.json
│   │   │   ├── feedback_injection_0094.json
│   │   │   ├── feedback_injection_0095.json
│   │   │   ├── feedback_injection_0096.json
│   │   │   ├── feedback_injection_0097.json
│   │   │   ├── feedback_injection_0098.json
│   │   │   ├── feedback_injection_0099.json
│   │   │   ├── feedback_injection_0100.json
│   │   │   ├── feedback_injection_0101.json
│   │   │   ├── feedback_injection_0102.json
│   │   │   ├── feedback_injection_0103.json
│   │   │   ├── feedback_injection_0104.json
│   │   │   ├── feedback_injection_0105.json
│   │   │   ├── feedback_injection_0106.json
│   │   │   ├── feedback_injection_0107.json
│   │   │   ├── feedback_injection_0108.json
│   │   │   ├── feedback_injection_0109.json
│   │   │   ├── feedback_injection_0110.json
│   │   │   ├── feedback_injection_0111.json
│   │   │   ├── feedback_injection_0112.json
│   │   │   ├── feedback_injection_0113.json
│   │   │   ├── feedback_injection_0114.json
│   │   │   ├── feedback_injection_0115.json
│   │   │   ├── feedback_injection_0116.json
│   │   │   ├── feedback_injection_0117.json
│   │   │   ├── feedback_injection_0118.json
│   │   │   ├── feedback_injection_0119.json
│   │   │   ├── feedback_injection_0120.json
│   │   │   ├── feedback_injection_0121.json
│   │   │   ├── feedback_injection_0122.json
│   │   │   └── feedback_injection_0123.json
│   │   ├── knowledge_delta
│   │   │   ├── knowledge_delta_0001.json
│   │   │   ├── knowledge_delta_0002.json
│   │   │   ├── knowledge_delta_0003.json
│   │   │   ├── knowledge_delta_0004.json
│   │   │   ├── knowledge_delta_0005.json
│   │   │   ├── knowledge_delta_0006.json
│   │   │   ├── knowledge_delta_0007.json
│   │   │   ├── knowledge_delta_0008.json
│   │   │   ├── knowledge_delta_0009.json
│   │   │   ├── knowledge_delta_0010.json
│   │   │   ├── knowledge_delta_0011.json
│   │   │   ├── knowledge_delta_0012.json
│   │   │   ├── knowledge_delta_0013.json
│   │   │   ├── knowledge_delta_0014.json
│   │   │   ├── knowledge_delta_0015.json
│   │   │   ├── knowledge_delta_0016.json
│   │   │   ├── knowledge_delta_0017.json
│   │   │   ├── knowledge_delta_0018.json
│   │   │   ├── knowledge_delta_0019.json
│   │   │   ├── knowledge_delta_0020.json
│   │   │   ├── knowledge_delta_0021.json
│   │   │   ├── knowledge_delta_0022.json
│   │   │   ├── knowledge_delta_0023.json
│   │   │   ├── knowledge_delta_0024.json
│   │   │   ├── knowledge_delta_0025.json
│   │   │   ├── knowledge_delta_0026.json
│   │   │   ├── knowledge_delta_0027.json
│   │   │   ├── knowledge_delta_0028.json
│   │   │   ├── knowledge_delta_0029.json
│   │   │   ├── knowledge_delta_0030.json
│   │   │   ├── knowledge_delta_0031.json
│   │   │   ├── knowledge_delta_0032.json
│   │   │   ├── knowledge_delta_0033.json
│   │   │   ├── knowledge_delta_0034.json
│   │   │   ├── knowledge_delta_0035.json
│   │   │   ├── knowledge_delta_0036.json
│   │   │   ├── knowledge_delta_0037.json
│   │   │   ├── knowledge_delta_0038.json
│   │   │   ├── knowledge_delta_0039.json
│   │   │   ├── knowledge_delta_0040.json
│   │   │   ├── knowledge_delta_0041.json
│   │   │   ├── knowledge_delta_0042.json
│   │   │   ├── knowledge_delta_0043.json
│   │   │   ├── knowledge_delta_0044.json
│   │   │   ├── knowledge_delta_0045.json
│   │   │   ├── knowledge_delta_0046.json
│   │   │   ├── knowledge_delta_0047.json
│   │   │   ├── knowledge_delta_0048.json
│   │   │   ├── knowledge_delta_0049.json
│   │   │   ├── knowledge_delta_0050.json
│   │   │   ├── knowledge_delta_0051.json
│   │   │   ├── knowledge_delta_0052.json
│   │   │   ├── knowledge_delta_0053.json
│   │   │   ├── knowledge_delta_0054.json
│   │   │   ├── knowledge_delta_0055.json
│   │   │   ├── knowledge_delta_0056.json
│   │   │   ├── knowledge_delta_0057.json
│   │   │   ├── knowledge_delta_0058.json
│   │   │   ├── knowledge_delta_0059.json
│   │   │   ├── knowledge_delta_0060.json
│   │   │   ├── knowledge_delta_0061.json
│   │   │   ├── knowledge_delta_0062.json
│   │   │   ├── knowledge_delta_0063.json
│   │   │   ├── knowledge_delta_0064.json
│   │   │   ├── knowledge_delta_0065.json
│   │   │   ├── knowledge_delta_0066.json
│   │   │   ├── knowledge_delta_0067.json
│   │   │   ├── knowledge_delta_0068.json
│   │   │   ├── knowledge_delta_0069.json
│   │   │   ├── knowledge_delta_0070.json
│   │   │   ├── knowledge_delta_0071.json
│   │   │   ├── knowledge_delta_0072.json
│   │   │   ├── knowledge_delta_0073.json
│   │   │   ├── knowledge_delta_0074.json
│   │   │   ├── knowledge_delta_0075.json
│   │   │   ├── knowledge_delta_0076.json
│   │   │   ├── knowledge_delta_0077.json
│   │   │   ├── knowledge_delta_0078.json
│   │   │   ├── knowledge_delta_0079.json
│   │   │   ├── knowledge_delta_0080.json
│   │   │   ├── knowledge_delta_0081.json
│   │   │   ├── knowledge_delta_0082.json
│   │   │   ├── knowledge_delta_0083.json
│   │   │   ├── knowledge_delta_0084.json
│   │   │   ├── knowledge_delta_0085.json
│   │   │   ├── knowledge_delta_0086.json
│   │   │   ├── knowledge_delta_0087.json
│   │   │   ├── knowledge_delta_0088.json
│   │   │   ├── knowledge_delta_0089.json
│   │   │   ├── knowledge_delta_0090.json
│   │   │   ├── knowledge_delta_0091.json
│   │   │   ├── knowledge_delta_0092.json
│   │   │   ├── knowledge_delta_0093.json
│   │   │   ├── knowledge_delta_0094.json
│   │   │   ├── knowledge_delta_0095.json
│   │   │   ├── knowledge_delta_0096.json
│   │   │   ├── knowledge_delta_0097.json
│   │   │   ├── knowledge_delta_0098.json
│   │   │   ├── knowledge_delta_0099.json
│   │   │   ├── knowledge_delta_0100.json
│   │   │   ├── knowledge_delta_0101.json
│   │   │   ├── knowledge_delta_0102.json
│   │   │   ├── knowledge_delta_0103.json
│   │   │   ├── knowledge_delta_0104.json
│   │   │   ├── knowledge_delta_0105.json
│   │   │   ├── knowledge_delta_0106.json
│   │   │   ├── knowledge_delta_0107.json
│   │   │   ├── knowledge_delta_0108.json
│   │   │   ├── knowledge_delta_0109.json
│   │   │   ├── knowledge_delta_0110.json
│   │   │   ├── knowledge_delta_0111.json
│   │   │   ├── knowledge_delta_0112.json
│   │   │   ├── knowledge_delta_0113.json
│   │   │   ├── knowledge_delta_0114.json
│   │   │   ├── knowledge_delta_0115.json
│   │   │   ├── knowledge_delta_0116.json
│   │   │   ├── knowledge_delta_0117.json
│   │   │   ├── knowledge_delta_0118.json
│   │   │   ├── knowledge_delta_0119.json
│   │   │   ├── knowledge_delta_0120.json
│   │   │   ├── knowledge_delta_0121.json
│   │   │   ├── knowledge_delta_0122.json
│   │   │   ├── knowledge_delta_0123.json
│   │   │   └── knowledge_delta_0124.json
│   │   ├── marketing_system
│   │   │   └── marketing_system_0001.json
│   │   ├── state_scoring
│   │   │   └── state_scoring_0001.json
│   │   ├── .gitkeep
│   │   ├── r_0003.json
│   │   ├── r_0004.json
│   │   ├── r_0005.json
│   │   ├── r_0006.json
│   │   ├── r_0007.json
│   │   ├── r_0008.json
│   │   ├── r_0009.json
│   │   ├── r_0010.json
│   │   ├── r_0011.json
│   │   ├── r_0012.json
│   │   ├── r_0013.json
│   │   ├── r_0014.json
│   │   ├── r_0015.json
│   │   ├── r_0016.json
│   │   ├── r_0017.json
│   │   ├── r_0018.json
│   │   ├── r_0019.json
│   │   ├── r_0020.json
│   │   ├── r_0021.json
│   │   ├── r_0022.json
│   │   ├── r_0023.json
│   │   ├── r_0024.json
│   │   ├── r_0025.json
│   │   ├── r_0026.json
│   │   ├── r_0027.json
│   │   ├── r_0028.json
│   │   ├── r_0029.json
│   │   ├── r_0030.json
│   │   ├── r_0031.json
│   │   ├── r_0032.json
│   │   ├── r_0033.json
│   │   ├── r_0034.json
│   │   ├── r_0035.json
│   │   ├── r_0036.json
│   │   ├── r_0037.json
│   │   ├── r_0038.json
│   │   ├── r_0039.json
│   │   ├── r_0040.json
│   │   ├── r_0041.json
│   │   ├── r_0042.json
│   │   ├── r_0043.json
│   │   ├── r_0044.json
│   │   ├── r_0045.json
│   │   ├── r_0046.json
│   │   ├── r_0047.json
│   │   ├── r_0048.json
│   │   ├── r_0049.json
│   │   ├── r_0050.json
│   │   ├── r_0051.json
│   │   ├── r_0052.json
│   │   ├── r_0053.json
│   │   ├── r_0054.json
│   │   ├── r_0055.json
│   │   ├── r_0056.json
│   │   ├── r_0057.json
│   │   ├── r_0058.json
│   │   ├── r_0059.json
│   │   ├── r_0060.json
│   │   ├── r_0061.json
│   │   ├── r_0062.json
│   │   ├── r_0063.json
│   │   ├── r_0064.json
│   │   ├── r_0065.json
│   │   ├── r_0066.json
│   │   ├── r_0067.json
│   │   ├── r_0068.json
│   │   ├── r_0069.json
│   │   ├── r_0070.json
│   │   ├── r_0071.json
│   │   ├── r_0072.json
│   │   ├── r_0073.json
│   │   ├── r_0074.json
│   │   ├── r_0075.json
│   │   ├── r_0076.json
│   │   ├── r_0077.json
│   │   ├── r_0078.json
│   │   ├── r_0079.json
│   │   ├── r_0080.json
│   │   ├── r_0081.json
│   │   ├── r_0082.json
│   │   ├── r_0083.json
│   │   ├── r_0084.json
│   │   ├── r_0085.json
│   │   ├── r_0086.json
│   │   ├── r_0087.json
│   │   ├── r_0088.json
│   │   ├── r_0089.json
│   │   ├── r_0090.json
│   │   ├── r_0091.json
│   │   ├── r_0092.json
│   │   ├── r_0093.json
│   │   ├── r_0094.json
│   │   ├── r_0095.json
│   │   ├── r_0096.json
│   │   ├── r_0097.json
│   │   ├── r_0098.json
│   │   ├── r_0099.json
│   │   ├── r_0100.json
│   │   ├── r_0101.json
│   │   ├── r_0102.json
│   │   ├── r_0103.json
│   │   ├── r_0104.json
│   │   ├── r_0105.json
│   │   ├── r_0106.json
│   │   ├── r_0107.json
│   │   ├── r_0108.json
│   │   ├── r_0109.json
│   │   ├── r_0110.json
│   │   ├── r_0111.json
│   │   ├── r_0112.json
│   │   ├── r_0113.json
│   │   ├── r_0114.json
│   │   ├── r_0115.json
│   │   ├── r_0116.json
│   │   ├── r_0117.json
│   │   ├── r_0118.json
│   │   ├── r_0119.json
│   │   ├── r_0120.json
│   │   ├── r_0121.json
│   │   ├── r_0122.json
│   │   ├── r_0123.json
│   │   ├── r_0124.json
│   │   ├── r_0125.json
│   │   ├── r_0126.json
│   │   ├── r_0127.json
│   │   ├── r_0128.json
│   │   ├── r_0129.json
│   │   ├── r_0130.json
│   │   ├── r_0131.json
│   │   ├── r_0132.json
│   │   ├── r_0133.json
│   │   ├── r_0134.json
│   │   ├── r_0135.json
│   │   ├── r_0136.json
│   │   ├── r_0137.json
│   │   ├── r_0138.json
│   │   ├── r_0139.json
│   │   ├── r_0140.json
│   │   ├── r_0141.json
│   │   ├── r_0142.json
│   │   ├── r_0143.json
│   │   ├── r_0144.json
│   │   ├── r_0145.json
│   │   ├── r_0146.json
│   │   ├── r_0147.json
│   │   ├── r_0148.json
│   │   ├── r_0149.json
│   │   ├── r_0150.json
│   │   ├── r_0151.json
│   │   ├── r_0152.json
│   │   ├── r_0153.json
│   │   ├── r_0154.json
│   │   ├── r_0155.json
│   │   ├── r_0156.json
│   │   ├── r_0157.json
│   │   ├── r_0158.json
│   │   ├── r_0159.json
│   │   ├── r_0160.json
│   │   ├── r_0161.json
│   │   ├── r_0162.json
│   │   ├── r_0163.json
│   │   ├── r_0164.json
│   │   ├── r_0165.json
│   │   ├── r_0166.json
│   │   ├── r_0167.json
│   │   ├── r_0168.json
│   │   ├── r_0169.json
│   │   ├── r_0170.json
│   │   ├── r_0171.json
│   │   ├── r_0172.json
│   │   ├── r_0173.json
│   │   ├── r_0174.json
│   │   ├── r_0175.json
│   │   ├── r_0176.json
│   │   ├── r_0177.json
│   │   ├── r_0178.json
│   │   ├── r_0179.json
│   │   ├── r_0180.json
│   │   ├── r_0181.json
│   │   ├── r_0182.json
│   │   ├── r_0183.json
│   │   ├── r_0184.json
│   │   ├── r_0185.json
│   │   ├── r_0186.json
│   │   ├── r_0187.json
│   │   └── r_0188.json
│   ├── replay
│   │   ├── .gitkeep
│   │   ├── c_0001.json
│   │   ├── c_0002.json
│   │   ├── c_0003.json
│   │   ├── c_0004.json
│   │   ├── c_0005.json
│   │   ├── c_0006.json
│   │   ├── c_0007.json
│   │   └── c_0008.json
│   ├── replication_plane
│   │   ├── experiment_replication_dispatcher.py
│   │   ├── replication_artifact_mirror.py
│   │   ├── replication_consensus_engine.py
│   │   ├── replication_disagreement_tracker.py
│   │   ├── replication_integrity_validator.py
│   │   ├── replication_peer_selector.py
│   │   ├── replication_publication_gate.py
│   │   ├── replication_queue_manager.py
│   │   ├── replication_result_merger.py
│   │   └── replication_stability_scanner.py
│   ├── result_delivery
│   │   ├── build_raw_data_bundle.py
│   │   ├── build_run_manifest.py
│   │   ├── build_standard_artifact_bundle.py
│   │   ├── publish_demo_summary.py
│   │   ├── request_raw_export.py
│   │   └── result_publication_profiles.json
│   ├── runtime
│   │   ├── active_feedback.json
│   │   ├── autonomous_loop_report.json
│   │   ├── distributed_worker_report.json
│   │   ├── execution_policy.json
│   │   ├── failure_recovery_report.json
│   │   ├── goal_execution_log.json
│   │   ├── pattern_memory.json
│   │   └── priority_weights.json
│   ├── sandbox_service
│   │   ├── api
│   │   │   └── README.md
│   │   ├── auth
│   │   │   └── README.md
│   │   ├── jobs
│   │   │   └── README.md
│   │   ├── adaptive_parallel_executor_stub.py
│   │   ├── adaptive_parallel_policy.json
│   │   ├── adaptive_run_allocator.py
│   │   ├── akash_deployment_adapter.py
│   │   ├── always_on_scheduler.py
│   │   ├── api_gateway.py
│   │   ├── artifact_access_auditor.py
│   │   ├── artifact_cdn_manifest.py
│   │   ├── artifact_compression_service.py
│   │   ├── artifact_distribution_router.py
│   │   ├── artifact_download_index.py
│   │   ├── artifact_integrity_verifier.py
│   │   ├── artifact_manifest_exporter.py
│   │   ├── artifact_merge_coordinator.py
│   │   ├── artifact_publication_router.py
│   │   ├── artifact_retention_manifest.py
│   │   ├── artifact_retention_scheduler.py
│   │   ├── artifact_signature_generator.py
│   │   ├── artifact_streaming_endpoint.py
│   │   ├── autonomous_claim_reviser.py
│   │   ├── autonomous_helpdesk_stub.py
│   │   ├── autonomous_paper_drafter.py
│   │   ├── autonomous_research_dashboard.py
│   │   ├── autonomous_run_reaper.py
│   │   ├── autonomous_run_trigger.py
│   │   ├── build_export_bundle.py
│   │   ├── bulk_dataset_exporter.py
│   │   ├── campaign_priority_queue.py
│   │   ├── campaign_publication_manifest.py
│   │   ├── campaign_result_publisher.py
│   │   ├── claim_evidence_linker.py
│   │   ├── cloud_execution_bridge.py
│   │   ├── compressed_dataset_notary.py
│   │   ├── compressed_raw_export_builder.py
│   │   ├── containerized_experiment_runner.py
│   │   ├── continuous_campaign_clock.py
│   │   ├── continuous_replication_manager.py
│   │   ├── continuous_uc_tracker.py
│   │   ├── cross_cluster_sync_engine.py
│   │   ├── cross_domain_dataset_router.py
│   │   ├── cross_repo_publication_router.py
│   │   ├── cross_repo_publish_stub.py
│   │   ├── dataset_access_control_stub.py
│   │   ├── dataset_access_controller.py
│   │   ├── dataset_exchange.py
│   │   ├── dataset_lineage_tracker.py
│   │   ├── dataset_mirror_manager.py
│   │   ├── dataset_permission_manager.py
│   │   ├── dataset_verification_notary.py
│   │   ├── dataset_version_registry.py
│   │   ├── delivery_profile_resolver.py
│   │   ├── demo_repo_push_coordinator.py
│   │   ├── distributed_campaign_coordinator.py
│   │   ├── distributed_compute_controller.py
│   │   ├── distributed_download_catalog.py
│   │   ├── distributed_notification_stub.py
│   │   ├── distributed_peer_validation_stub.py
│   │   ├── distributed_run_query_api.py
│   │   ├── distributed_validation_dispatcher.py
│   │   ├── doi_generator.py
│   │   ├── drift_alarm_router.py
│   │   ├── experiment_bundle_builder.py
│   │   ├── experiment_cost_estimator.py
│   │   ├── experiment_cost_meter.py
│   │   ├── experiment_download_api.py
│   │   ├── experiment_export_api_stub.py
│   │   ├── experiment_job_scheduler.py
│   │   ├── experiment_marketplace.py
│   │   ├── experiment_metadata_query.py
│   │   ├── experiment_mode_preflight_checker.py
│   │   ├── experiment_result_stream.py
│   │   ├── experiment_submission_api.py
│   │   ├── falsification_report_publisher.py
│   │   ├── federated_artifact_access_auditor.py
│   │   ├── federated_run_request_api.py
│   │   ├── federation_node_connector.py
│   │   ├── federation_sync_engine.py
│   │   ├── final_results_zip_builder.py
│   │   ├── global_invariant_feed.py
│   │   ├── global_science_status_board.py
│   │   ├── gpu_cluster_adapter.py
│   │   ├── invariant_model_registry.py
│   │   ├── invariant_publication_router.py
│   │   ├── invariant_registry_public.py
│   │   ├── invariant_result_catalog.py
│   │   ├── live_boundary_monitor.py
│   │   ├── matrix_shard_builder.py
│   │   ├── merge_job_trigger_stub.py
│   │   ├── multi_tenant_quota_router.py
│   │   ├── network_dashboard_api.py
│   │   ├── networkwide_consistency_guard.py
│   │   ├── node_capability_query_api.py
│   │   ├── open_dataset_mirror.py
│   │   ├── parallel_artifact_downloader.py
│   │   ├── parallel_artifact_uploader.py
│   │   ├── parallel_merge_manifest_builder.py
│   │   ├── parallel_result_merger.py
│   │   ├── parallel_run_executor_stub.py
│   │   ├── parallel_run_mode_resolver.py
│   │   ├── peer_bundle_exchange.py
│   │   ├── peer_dataset_request_handler.py
│   │   ├── peer_review_bundle_builder.py
│   │   ├── public_dataset_catalog.py
│   │   ├── public_result_search.py
│   │   ├── publication_export_service.py
│   │   ├── quota_enforcer.py
│   │   ├── raw_export_request_handler.py
│   │   ├── raw_export_request_registry.py
│   │   ├── raw_export_retention_policy.py
│   │   ├── README.md
│   │   ├── remote_job_queue.py
│   │   ├── remote_pipeline_trigger.py
│   │   ├── remote_result_collector.py
│   │   ├── replication_job_board.py
│   │   ├── replication_request_api.py
│   │   ├── reproducible_experiment_publisher.py
│   │   ├── research_claim_registry.py
│   │   ├── research_cloud_api.py
│   │   ├── research_delivery_contract.json
│   │   ├── research_delivery_dashboard.py
│   │   ├── research_identity_manager.py
│   │   ├── research_network_dashboard.py
│   │   ├── research_network_status_api.py
│   │   ├── research_node_registration_api.py
│   │   ├── research_package_export.py
│   │   ├── research_provenance_engine.py
│   │   ├── research_publication_pipeline.py
│   │   ├── research_workspace_api.py
│   │   ├── research_workspace_manager.py
│   │   ├── researcher_delivery_preferences.py
│   │   ├── researcher_invariant_query_api.py
│   │   ├── researcher_notification_stub.py
│   │   ├── researcher_request_auditor.py
│   │   ├── researcher_workspace_api.py
│   │   ├── result_bundle_download_index.py
│   │   ├── result_delivery_profiles_901.json
│   │   ├── result_integrity_checker.py
│   │   ├── result_manifest_api_stub.py
│   │   ├── result_publication_scheduler.py
│   │   ├── result_replication_controller.py
│   │   ├── result_stream_processor.py
│   │   ├── run_mode_schema.json
│   │   ├── run_status_api_stub.py
│   │   ├── sandbox_billing_adapter.py
│   │   ├── sandbox_node_registry.py
│   │   ├── sandbox_resource_quota.py
│   │   ├── sandbox_service_request_schema.json
│   │   ├── sandbox_session_manager.py
│   │   ├── science_cloud_dashboard.py
│   │   ├── service_api_gateway.py
│   │   ├── service_health_monitor.py
│   │   ├── service_metrics_exporter.py
│   │   ├── service_result_catalog.py
│   │   ├── shard_capacity_estimator.py
│   │   ├── shard_seed_allocator.py
│   │   ├── single_run_executor_stub.py
│   │   ├── symbolic_result_exporter.py
│   │   ├── user_quota_dashboard.py
│   │   ├── user_result_delivery_profile.py
│   │   ├── user_workspace_manager.py
│   │   ├── workflow_dispatch_profile_manager.py
│   │   ├── workflow_execution_plan.json
│   │   ├── workflow_execution_plan_builder.py
│   │   ├── workflow_mode_selector.py
│   │   ├── workflow_runner_bridge.py
│   │   └── workspace_provisioner.py
│   ├── security_plane
│   │   ├── crypto
│   │   │   ├── pq_hash.py
│   │   │   ├── pq_signatures.py
│   │   │   ├── provider.py
│   │   │   └── README.md
│   │   ├── integrity
│   │   │   ├── hash_chain.py
│   │   │   └── README.md
│   │   ├── key_registry
│   │   │   └── authority_keys.json
│   │   ├── .gitkeep
│   │   └── README.md
│   ├── state_scoring
│   │   ├── state_score.json
│   │   └── state_score.md
│   ├── upgrades
│   │   ├── README.md
│   │   └── UPGRADE_LIST.md
│   ├── workflows
│   │   ├── promote_staged_workflows.yml
│   │   └── run_evaluation.yml
│   ├── Architecture_Diagram_v2.pdf
│   ├── architecture_map.md
│   ├── canonical_manifest_template.json
│   ├── decision_state_recorder.py
│   ├── diagram.md
│   ├── example.py
│   ├── loop_state.json
│   ├── README.md
│   ├── receipt_chain.py
│   ├── stability_governor.py
│   ├── StegVerse_Formal_Spec_v2.pdf
│   └── system_manifest.json
├── publication_plane
│   ├── artifact_archive_builder.py
│   ├── artifact_bundle_signer.py
│   ├── autonomous_publication_gate.py
│   ├── citation_trace_exporter.py
│   ├── claim_to_figure_linker.py
│   ├── dataset_bundle_publisher.py
│   ├── dataset_doi_stub.py
│   ├── demo_latest_pointer_builder.py
│   ├── demo_repo_sync_agent.py
│   ├── demo_surface_sync_agent.py
│   ├── evidence_appendix_builder.py
│   ├── export_demo_pipeline.py
│   ├── external_dataset_exporter.py
│   ├── figure_manifest_builder.py
│   ├── global_registry_sync_agent.py
│   ├── merge_summary_publisher.py
│   ├── methodology_packet_exporter.py
│   ├── open_data_catalog_updater.py
│   ├── open_review_packet_builder.py
│   ├── paper_outline_synthesizer.py
│   ├── press_summary_generator.py
│   ├── public_dashboard_snapshotter.py
│   ├── public_summary_page_builder.py
│   ├── publication_health_monitor.py
│   ├── publication_receipt_writer.py
│   ├── publication_summary_builder.py
│   ├── publish_demo_surface.py
│   ├── release_channel_router.py
│   ├── replication_badge_generator.py
│   ├── replication_badge_publisher.py
│   ├── research_publication_router.py
│   ├── research_release_manager.py
│   ├── research_release_notary.py
│   ├── result_snapshot_builder.py
│   ├── results_readme_refresher.py
│   ├── review_round_tracker.py
│   ├── summary_card_builder.py
│   ├── table_packager.py
│   └── user_facing_result_packet_builder.py
├── receipts
│   ├── install_receipt_20260315_172736.json
│   ├── install_receipt_20260317_153531.json
│   ├── install_receipt_20260317_153732.json
│   ├── install_receipt_20260317_155003.json
│   ├── install_receipt_20260317_193822.json
│   ├── install_receipt_20260317_194525.json
│   ├── install_receipt_20260322_215155.json
│   └── README.md
├── replication_plane
│   ├── experiment_replication_dispatcher.py
│   ├── replication_artifact_mirror.py
│   ├── replication_consensus_engine.py
│   ├── replication_disagreement_tracker.py
│   ├── replication_integrity_validator.py
│   ├── replication_peer_selector.py
│   ├── replication_publication_gate.py
│   ├── replication_queue_manager.py
│   ├── replication_result_merger.py
│   └── replication_stability_scanner.py
├── reports
│   └── README.md
├── reproducibility
│   ├── __init__.py
│   └── bundle_builder.py
├── result_delivery
│   ├── build_raw_data_bundle.py
│   ├── build_run_manifest.py
│   ├── build_standard_artifact_bundle.py
│   ├── publish_demo_summary.py
│   ├── request_raw_export.py
│   └── result_publication_profiles.json
├── results
│   └── README.md
├── runner
│   ├── __init__.py
│   ├── aggregate_builder.py
│   ├── auto_runner.py
│   ├── build_all_artifacts.py
│   ├── data_collector.py
│   ├── example_results.txt
│   ├── handoff.py
│   ├── orchestrator.py
│   ├── receipts.py
│   ├── report_index.py
│   ├── report_writer.py
│   ├── result_writer.py
│   ├── scenario_loader.py
│   └── visualize_run.py
├── safe-ingestion-upgrade-bundle
│   ├── failed_bundles
│   │   └── .gitkeep
│   ├── ingestion
│   │   ├── classify_bundle_contents.py
│   │   ├── find_all_bundles.py
│   │   ├── ingest_bundle_safe.py
│   │   ├── move_processed_bundle.py
│   │   ├── verify_installation.py
│   │   └── write_install_report.py
│   ├── installed_bundles
│   │   └── .gitkeep
│   ├── workflow_review
│   │   └── .gitkeep
│   └── README.md
├── sandbox
│   ├── __init__.py
│   ├── entity_state.py
│   ├── event_bus.py
│   ├── mutation_injector.py
│   ├── phase_space.py
│   ├── scheduler.py
│   └── trust_drift.py
├── sandbox_service
│   ├── api
│   │   └── README.md
│   ├── auth
│   │   └── README.md
│   ├── jobs
│   │   └── README.md
│   ├── adaptive_parallel_executor_stub.py
│   ├── adaptive_parallel_policy.json
│   ├── adaptive_run_allocator.py
│   ├── akash_deployment_adapter.py
│   ├── always_on_scheduler.py
│   ├── api_gateway.py
│   ├── artifact_access_auditor.py
│   ├── artifact_cdn_manifest.py
│   ├── artifact_compression_service.py
│   ├── artifact_distribution_router.py
│   ├── artifact_download_index.py
│   ├── artifact_integrity_verifier.py
│   ├── artifact_manifest_exporter.py
│   ├── artifact_merge_coordinator.py
│   ├── artifact_publication_router.py
│   ├── artifact_retention_manifest.py
│   ├── artifact_retention_scheduler.py
│   ├── artifact_signature_generator.py
│   ├── artifact_streaming_endpoint.py
│   ├── autonomous_claim_reviser.py
│   ├── autonomous_helpdesk_stub.py
│   ├── autonomous_paper_drafter.py
│   ├── autonomous_research_dashboard.py
│   ├── autonomous_run_reaper.py
│   ├── autonomous_run_trigger.py
│   ├── build_export_bundle.py
│   ├── bulk_dataset_exporter.py
│   ├── campaign_priority_queue.py
│   ├── campaign_publication_manifest.py
│   ├── campaign_result_publisher.py
│   ├── claim_evidence_linker.py
│   ├── cloud_execution_bridge.py
│   ├── compressed_dataset_notary.py
│   ├── compressed_raw_export_builder.py
│   ├── containerized_experiment_runner.py
│   ├── continuous_campaign_clock.py
│   ├── continuous_replication_manager.py
│   ├── continuous_uc_tracker.py
│   ├── cross_cluster_sync_engine.py
│   ├── cross_domain_dataset_router.py
│   ├── cross_repo_publication_router.py
│   ├── cross_repo_publish_stub.py
│   ├── dataset_access_control_stub.py
│   ├── dataset_access_controller.py
│   ├── dataset_exchange.py
│   ├── dataset_lineage_tracker.py
│   ├── dataset_mirror_manager.py
│   ├── dataset_permission_manager.py
│   ├── dataset_verification_notary.py
│   ├── dataset_version_registry.py
│   ├── delivery_profile_resolver.py
│   ├── demo_repo_push_coordinator.py
│   ├── distributed_campaign_coordinator.py
│   ├── distributed_compute_controller.py
│   ├── distributed_download_catalog.py
│   ├── distributed_notification_stub.py
│   ├── distributed_peer_validation_stub.py
│   ├── distributed_run_query_api.py
│   ├── distributed_validation_dispatcher.py
│   ├── doi_generator.py
│   ├── drift_alarm_router.py
│   ├── experiment_bundle_builder.py
│   ├── experiment_cost_estimator.py
│   ├── experiment_cost_meter.py
│   ├── experiment_download_api.py
│   ├── experiment_export_api_stub.py
│   ├── experiment_job_scheduler.py
│   ├── experiment_marketplace.py
│   ├── experiment_metadata_query.py
│   ├── experiment_mode_preflight_checker.py
│   ├── experiment_result_stream.py
│   ├── experiment_submission_api.py
│   ├── falsification_report_publisher.py
│   ├── federated_artifact_access_auditor.py
│   ├── federated_run_request_api.py
│   ├── federation_node_connector.py
│   ├── federation_sync_engine.py
│   ├── final_results_zip_builder.py
│   ├── global_invariant_feed.py
│   ├── global_science_status_board.py
│   ├── gpu_cluster_adapter.py
│   ├── invariant_model_registry.py
│   ├── invariant_publication_router.py
│   ├── invariant_registry_public.py
│   ├── invariant_result_catalog.py
│   ├── live_boundary_monitor.py
│   ├── matrix_shard_builder.py
│   ├── merge_job_trigger_stub.py
│   ├── multi_tenant_quota_router.py
│   ├── network_dashboard_api.py
│   ├── networkwide_consistency_guard.py
│   ├── node_capability_query_api.py
│   ├── open_dataset_mirror.py
│   ├── parallel_artifact_downloader.py
│   ├── parallel_artifact_uploader.py
│   ├── parallel_merge_manifest_builder.py
│   ├── parallel_result_merger.py
│   ├── parallel_run_executor_stub.py
│   ├── parallel_run_mode_resolver.py
│   ├── peer_bundle_exchange.py
│   ├── peer_dataset_request_handler.py
│   ├── peer_review_bundle_builder.py
│   ├── public_dataset_catalog.py
│   ├── public_result_search.py
│   ├── publication_export_service.py
│   ├── quota_enforcer.py
│   ├── raw_export_request_handler.py
│   ├── raw_export_request_registry.py
│   ├── raw_export_retention_policy.py
│   ├── README.md
│   ├── remote_job_queue.py
│   ├── remote_pipeline_trigger.py
│   ├── remote_result_collector.py
│   ├── replication_job_board.py
│   ├── replication_request_api.py
│   ├── reproducible_experiment_publisher.py
│   ├── research_claim_registry.py
│   ├── research_cloud_api.py
│   ├── research_delivery_contract.json
│   ├── research_delivery_dashboard.py
│   ├── research_identity_manager.py
│   ├── research_network_dashboard.py
│   ├── research_network_status_api.py
│   ├── research_node_registration_api.py
│   ├── research_package_export.py
│   ├── research_provenance_engine.py
│   ├── research_publication_pipeline.py
│   ├── research_workspace_api.py
│   ├── research_workspace_manager.py
│   ├── researcher_delivery_preferences.py
│   ├── researcher_invariant_query_api.py
│   ├── researcher_notification_stub.py
│   ├── researcher_request_auditor.py
│   ├── researcher_workspace_api.py
│   ├── result_bundle_download_index.py
│   ├── result_delivery_profiles_901.json
│   ├── result_integrity_checker.py
│   ├── result_manifest_api_stub.py
│   ├── result_publication_scheduler.py
│   ├── result_replication_controller.py
│   ├── result_stream_processor.py
│   ├── run_mode_schema.json
│   ├── run_status_api_stub.py
│   ├── sandbox_billing_adapter.py
│   ├── sandbox_node_registry.py
│   ├── sandbox_resource_quota.py
│   ├── sandbox_service_request_schema.json
│   ├── sandbox_session_manager.py
│   ├── science_cloud_dashboard.py
│   ├── service_api_gateway.py
│   ├── service_health_monitor.py
│   ├── service_metrics_exporter.py
│   ├── service_result_catalog.py
│   ├── shard_capacity_estimator.py
│   ├── shard_seed_allocator.py
│   ├── single_run_executor_stub.py
│   ├── symbolic_result_exporter.py
│   ├── user_quota_dashboard.py
│   ├── user_result_delivery_profile.py
│   ├── user_workspace_manager.py
│   ├── workflow_dispatch_profile_manager.py
│   ├── workflow_execution_plan.json
│   ├── workflow_execution_plan_builder.py
│   ├── workflow_mode_selector.py
│   ├── workflow_runner_bridge.py
│   └── workspace_provisioner.py
├── sandbox_service_upgrades_451_482_v1
│   ├── install
│   │   └── install_bundle_autoregister.py
│   ├── payload
│   │   └── sandbox_service
│   │       ├── akash_deployment_adapter.py
│   │       ├── api_gateway.py
│   │       ├── cloud_execution_bridge.py
│   │       ├── containerized_experiment_runner.py
│   │       ├── dataset_exchange.py
│   │       ├── dataset_permission_manager.py
│   │       ├── dataset_version_registry.py
│   │       ├── distributed_compute_controller.py
│   │       ├── doi_generator.py
│   │       ├── experiment_bundle_builder.py
│   │       ├── experiment_cost_meter.py
│   │       ├── experiment_job_scheduler.py
│   │       ├── experiment_marketplace.py
│   │       ├── experiment_result_stream.py
│   │       ├── experiment_submission_api.py
│   │       ├── federation_node_connector.py
│   │       ├── federation_sync_engine.py
│   │       ├── gpu_cluster_adapter.py
│   │       ├── invariant_registry_public.py
│   │       ├── public_dataset_catalog.py
│   │       ├── remote_pipeline_trigger.py
│   │       ├── reproducible_experiment_publisher.py
│   │       ├── research_identity_manager.py
│   │       ├── research_package_export.py
│   │       ├── researcher_workspace_api.py
│   │       ├── sandbox_billing_adapter.py
│   │       ├── sandbox_node_registry.py
│   │       ├── sandbox_resource_quota.py
│   │       ├── sandbox_session_manager.py
│   │       ├── service_health_monitor.py
│   │       ├── user_quota_dashboard.py
│   │       └── user_workspace_manager.py
│   ├── bundle_manifest.json
│   └── bundle_readme.md
├── sandbox_worker_node
│   └── worker.py
├── sdk
│   ├── __init__.py
│   ├── DEFINITIONS_REVIEW.json
│   └── README.md
├── security_plane
│   ├── crypto
│   │   ├── pq_hash.py
│   │   ├── pq_signatures.py
│   │   ├── provider.py
│   │   └── README.md
│   ├── integrity
│   │   ├── hash_chain.py
│   │   └── README.md
│   ├── key_registry
│   │   └── authority_keys.json
│   ├── .gitkeep
│   └── README.md
├── statistics
│   ├── __init__.py
│   ├── collapse_probability_estimator.py
│   └── multi_trial_runner.py
├── tests
│   ├── test_failure_feedback.py
│   ├── test_priority_router.py
│   ├── test_self_improve.py
│   └── test_spec_quality.py
├── visualization
│   ├── __init__.py
│   └── phase_map_builder.py
├── workflow-review-classifier-bundle
│   ├── ingestion
│   │   └── compare_workflows.py
│   ├── workflow_deprecated
│   │   └── .gitkeep
│   ├── workflow_replace
│   │   └── .gitkeep
│   ├── integration_notes.md
│   └── README.md
├── workflow_review
│   ├── safe-ingestion-upgrade-bundle
│   │   └── .github
│   │       └── workflows
│   │           └── safe-ingest-all-bundles.yml
│   ├── .gitkeep
│   ├── auto-ingest-bundle.yml
│   ├── BUILD_NOTES.md
│   ├── CANONICAL_LOOP_NOTES_V1.md
│   ├── CANONICAL_LOOP_WORKFLOW_V1.yml.txt
│   ├── DOCUMENT_ENGINE_INSTALL_NOTES_V21_2A.md
│   ├── DOCUMENT_ENGINE_WORKFLOW_V21_2A.yml.txt
│   ├── EVAL_NOTES.md
│   ├── EVAL_WIRING_PATCH.md
│   ├── forward_build_notes.md
│   ├── installation_notes.md
│   ├── IPHONE_NO_CLI_PROMOTER_WORKFLOW_NOTES.md
│   ├── JSON_SAFE_FIX_NOTES.md
│   ├── LIFECYCLE_AUTH_NOTES.md
│   ├── NOTES.md
│   ├── PROMOTION_RECEIPTS_DIFF_VISIBILITY_V1.md
│   ├── PUBLICATION_ENGINE_NOTES_V21_3A.md
│   ├── REPO_ROOT_PROMOTER_V1.md
│   ├── run.yml
│   ├── safe-ingest-all-bundles.yml
│   ├── V14_3_TO_V15_NOTES.md
│   ├── V20_1_PREFLIGHT_NOTES.md
│   ├── V21_NOTES.md
│   ├── V6_2_SHARED_STATE_PATCH.md
│   ├── V6_3_WORKFLOW_REVIEW.md
│   ├── V6_4_REVIEW.md
│   ├── V6_5_NO_CLI_AUTOMATION.md
│   ├── V7_README.md
│   └── V8_NOTES.md
├── .gitignore
├── api_server.py
├── app.py
├── authority_resolver.py
├── autonomous_runtime.py
├── bootstrap_installer.py
├── bundle_auto_repair.py
├── bundle_manifest.json
├── combined_bundle_manifest.json
├── consensus_check.py
├── decision_engine.py
├── decision_state_recorder.py
├── decision_verifier.py
├── entity_sandbox_phase_space_bundle.zip
├── entity_sandbox_runner_github_bundle.zip
├── epoch_compactor.py
├── example.py
├── executor.py
├── failure_recovery_bundle_v1.zip
├── governed_executor.py
├── invariant_checker.py
├── job_listener.py
├── merkle_compactor.py
├── module_registry.json
├── multi_node_verifier.py
├── node_recovery.py
├── predictive_engine.py
├── PROPOSED_BUILD.md
├── README.md
├── README_COMBINED_BUNDLE.md
├── receipt_chain.py
├── receipt_chain_verifier.py
├── receipt_gossip.py
├── receipt_schema.json
├── replay_engine.py
├── requirements.txt
├── retry_policy.py
├── rigel_number.zip
├── run_repro_bundle.py
├── run_visualizations.py
├── runtime_guardian.py
├── sandbox_research_upgrades_151_165_v1.zip
├── shard_lock_manager.py
├── shard_reliability_lock_bundle_v1.zip
├── stability_governor.py
├── state_hash.py
├── state_reconstructor.py
├── stegcge_closure_modules_v1_bundle.zip
├── system_manifest.json
├── test_adversarial_node.py
├── test_api.py
├── test_decision_engine.py
├── test_governed_executor.py
├── test_multi_node_verification.py
├── test_replay_system.py
├── test_state_reconstruction.py
├── test_tamper_block.py
├── u_signal_monitor.py
├── UPGRADE_INSTRUCTIONS.md
└── weighted_consensus.py
```
