"""Stability governor for the StegVerse Research Sandbox.

Suggested placement:
    control_plane/stability_governor.py

Consumes samples from observation_plane.u_signal_monitor.USignalMonitor and
returns deterministic control actions for sandbox orchestration.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class GovernorDecision:
    region: str
    action_mode: str
    actions: List[str]
    severity: str
    reason: str
    dominant_driver: str
    predicted_boundary_crossing: bool


class StabilityGovernor:
    """Maps U-signal state into concrete control decisions."""

    def __init__(
        self,
        forecast_boundary: float = 0.0,
        caution_velocity_threshold: float = -0.03,
        critical_velocity_threshold: float = -0.08,
        unstable_velocity_threshold: float = -0.15,
    ) -> None:
        self.forecast_boundary = forecast_boundary
        self.caution_velocity_threshold = caution_velocity_threshold
        self.critical_velocity_threshold = critical_velocity_threshold
        self.unstable_velocity_threshold = unstable_velocity_threshold

    def decide(self, sample) -> GovernorDecision:
        predicted_crossing = sample.forecast_margin <= self.forecast_boundary
        region = sample.region
        velocity = sample.velocity
        dominant_driver = sample.dominant_driver

        if region == 'healthy':
            return GovernorDecision(
                region=region,
                action_mode='normal_operation',
                actions=['allow_new_jobs', 'standard_sampling', 'record_health_state'],
                severity='low',
                reason='Stability margin remains above the healthy operating band.',
                dominant_driver=dominant_driver,
                predicted_boundary_crossing=predicted_crossing,
            )

        if region == 'caution':
            actions = ['increase_sampling_rate', 'soft_throttle_low_priority_jobs', 'record_caution_event']
            if predicted_crossing or velocity <= self.caution_velocity_threshold:
                actions.extend(['raise_validator_capacity', 'checkpoint_active_workspaces'])
            return GovernorDecision(
                region=region,
                action_mode='soft_throttle',
                actions=actions,
                severity='medium',
                reason='The system is above the critical surface but trending toward reduced stability.',
                dominant_driver=dominant_driver,
                predicted_boundary_crossing=predicted_crossing,
            )

        if region == 'critical':
            actions = [
                'freeze_high_risk_jobs',
                'require_authority_rederivation',
                'raise_validation_strictness',
                'checkpoint_active_workspaces',
                'record_critical_event',
            ]
            if predicted_crossing or velocity <= self.critical_velocity_threshold:
                actions.extend(['pause_nonessential_experiments', 'prepare_recovery_mode'])
            return GovernorDecision(
                region=region,
                action_mode='critical_control',
                actions=actions,
                severity='high',
                reason='The system has approached the critical surface and requires intervention.',
                dominant_driver=dominant_driver,
                predicted_boundary_crossing=predicted_crossing,
            )

        actions = [
            'hard_throttle_all_nonessential_execution',
            'deny_new_high_risk_jobs',
            'force_checkpoint_and_evidence_flush',
            'require_manual_review_gate',
            'enter_recovery_mode',
            'record_unstable_event',
        ]
        if predicted_crossing or velocity <= self.unstable_velocity_threshold:
            actions.append('trigger_operator_alert')
        return GovernorDecision(
            region=region,
            action_mode='recovery_mode',
            actions=actions,
            severity='critical',
            reason='The system is operating beyond the safe stability margin.',
            dominant_driver=dominant_driver,
            predicted_boundary_crossing=predicted_crossing,
        )

    @staticmethod
    def integrate_with_runner_payload(decision: GovernorDecision) -> Dict[str, object]:
        return asdict(decision)
