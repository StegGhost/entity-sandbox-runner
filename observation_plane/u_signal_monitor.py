"""Live U-signal monitor for the StegVerse Research Sandbox.

Suggested placement:
    observation_plane/u_signal_monitor.py

This module turns the candidate invariant
    U = (capacity * continuity) / (pressure * constraints)
into a measurable control signal with margin, velocity, acceleration,
and short-horizon forecasting.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from collections import deque
from typing import Callable, Deque, Dict, List, Optional
import math
import time


@dataclass
class MetricSample:
    timestamp: float
    capacity: float
    continuity: float
    pressure: float
    constraints: float
    u_value: float
    margin: float
    velocity: float
    acceleration: float
    forecast_margin: float
    region: str
    dominant_driver: str


class USignalMonitor:
    """Computes live stability metrics for sandbox experiments.

    The primary control signal is:
        margin = log(U)
    where U = (capacity * continuity) / (pressure * constraints)

    Region interpretation:
        healthy  -> margin > healthy_margin
        caution  -> 0 < margin <= healthy_margin
        critical -> -critical_margin <= margin <= 0
        unstable -> margin < -critical_margin
    """

    def __init__(
        self,
        healthy_margin: float = 0.40,
        critical_margin: float = 0.20,
        forecast_horizon: float = 3.0,
        history_size: int = 64,
        epsilon: float = 1e-9,
        weights: Optional[Dict[str, float]] = None,
    ) -> None:
        self.healthy_margin = healthy_margin
        self.critical_margin = critical_margin
        self.forecast_horizon = forecast_horizon
        self.history: Deque[MetricSample] = deque(maxlen=history_size)
        self.epsilon = epsilon
        self.weights = weights or {
            'capacity': 1.0,
            'continuity': 1.0,
            'pressure': 1.0,
            'constraints': 1.0,
        }

    @staticmethod
    def _clamp_positive(value: float, epsilon: float) -> float:
        return max(float(value), epsilon)

    def compute_u(self, capacity: float, continuity: float, pressure: float, constraints: float) -> float:
        c = self._clamp_positive(capacity, self.epsilon) ** self.weights['capacity']
        t = self._clamp_positive(continuity, self.epsilon) ** self.weights['continuity']
        p = self._clamp_positive(pressure, self.epsilon) ** self.weights['pressure']
        k = self._clamp_positive(constraints, self.epsilon) ** self.weights['constraints']
        return (c * t) / max(p * k, self.epsilon)

    def compute_margin(self, u_value: float) -> float:
        return math.log(self._clamp_positive(u_value, self.epsilon))

    def classify_region(self, margin: float) -> str:
        if margin > self.healthy_margin:
            return 'healthy'
        if 0.0 < margin <= self.healthy_margin:
            return 'caution'
        if -self.critical_margin <= margin <= 0.0:
            return 'critical'
        return 'unstable'

    def _compute_derivatives(self, margin: float, timestamp: float) -> tuple[float, float]:
        velocity = 0.0
        acceleration = 0.0
        if len(self.history) >= 1:
            prev = self.history[-1]
            dt = max(timestamp - prev.timestamp, self.epsilon)
            velocity = (margin - prev.margin) / dt
        if len(self.history) >= 2:
            prev2 = self.history[-2]
            prev1 = self.history[-1]
            dt_prev = max(prev1.timestamp - prev2.timestamp, self.epsilon)
            prev_velocity = (prev1.margin - prev2.margin) / dt_prev
            dt_now = max(timestamp - prev1.timestamp, self.epsilon)
            velocity = (margin - prev1.margin) / dt_now
            acceleration = (velocity - prev_velocity) / max((dt_prev + dt_now) / 2.0, self.epsilon)
        return velocity, acceleration

    def forecast_margin(self, margin: float, velocity: float, acceleration: float) -> float:
        tau = self.forecast_horizon
        return margin + tau * velocity + 0.5 * tau * tau * acceleration

    def identify_dominant_driver(
        self,
        capacity: float,
        continuity: float,
        pressure: float,
        constraints: float,
    ) -> str:
        # Lower numerator terms and higher denominator terms both reduce stability.
        signals = {
            'capacity_deficit': 1.0 / self._clamp_positive(capacity, self.epsilon),
            'continuity_loss': 1.0 / self._clamp_positive(continuity, self.epsilon),
            'pressure_spike': self._clamp_positive(pressure, self.epsilon),
            'constraint_burden': self._clamp_positive(constraints, self.epsilon),
        }
        return max(signals, key=signals.get)

    def update(
        self,
        capacity: float,
        continuity: float,
        pressure: float,
        constraints: float,
        timestamp: Optional[float] = None,
    ) -> MetricSample:
        ts = float(time.time() if timestamp is None else timestamp)
        u_value = self.compute_u(capacity, continuity, pressure, constraints)
        margin = self.compute_margin(u_value)
        velocity, acceleration = self._compute_derivatives(margin, ts)
        forecast = self.forecast_margin(margin, velocity, acceleration)
        region = self.classify_region(margin)
        dominant_driver = self.identify_dominant_driver(capacity, continuity, pressure, constraints)

        sample = MetricSample(
            timestamp=ts,
            capacity=capacity,
            continuity=continuity,
            pressure=pressure,
            constraints=constraints,
            u_value=u_value,
            margin=margin,
            velocity=velocity,
            acceleration=acceleration,
            forecast_margin=forecast,
            region=region,
            dominant_driver=dominant_driver,
        )
        self.history.append(sample)
        return sample

    def snapshot(self) -> Dict[str, object]:
        current = asdict(self.history[-1]) if self.history else None
        return {
            'healthy_margin': self.healthy_margin,
            'critical_margin': self.critical_margin,
            'forecast_horizon': self.forecast_horizon,
            'history_size': len(self.history),
            'current': current,
        }

    def history_as_dicts(self) -> List[Dict[str, object]]:
        return [asdict(item) for item in self.history]


def compute_metrics_from_mapping(mapping: Dict[str, float]) -> Dict[str, float]:
    """Utility adapter for sandbox code that already emits metric dictionaries."""
    required = ('governance_capacity', 'trust_continuity', 'artifact_pressure', 'constraints')
    missing = [key for key in required if key not in mapping]
    if missing:
        raise KeyError(f'Missing required metrics: {missing}')
    return {
        'capacity': float(mapping['governance_capacity']),
        'continuity': float(mapping['trust_continuity']),
        'pressure': float(mapping['artifact_pressure']),
        'constraints': float(mapping['constraints']),
    }
