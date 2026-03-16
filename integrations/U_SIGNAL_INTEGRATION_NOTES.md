# Combined Bundle Notes

This bundle combines:
- sandbox_service_upgrades_451_482_v1
- sandbox_readme_updates_v2
- drop-in U-signal control files

## New files added

- `observation_plane/u_signal_monitor.py`
- `control_plane/stability_governor.py`
- `integrations/U_SIGNAL_INTEGRATION_NOTES.md`
- `PROPOSED_BUILD.md`

## Suggested wiring

1. Import `USignalMonitor` in your sandbox runner.
2. Import `StabilityGovernor` in your control-plane orchestration path.
3. On each experiment cycle:
   - collect `governance_capacity`
   - collect `trust_continuity`
   - collect `artifact_pressure`
   - collect `constraints`
4. Feed those values into `USignalMonitor.update(...)`.
5. Pass the returned sample into `StabilityGovernor.decide(sample)`.
6. Write both the sample and the decision to your evidence plane.

## Suggested placement

- `observation_plane/u_signal_monitor.py`
- `control_plane/stability_governor.py`

## Minimal example

```python
from observation_plane.u_signal_monitor import USignalMonitor
from control_plane.stability_governor import StabilityGovernor

monitor = USignalMonitor()
governor = StabilityGovernor()

sample = monitor.update(
    capacity=0.82,
    continuity=0.91,
    pressure=0.64,
    constraints=0.70,
)

decision = governor.decide(sample)
print(sample)
print(decision)
```
