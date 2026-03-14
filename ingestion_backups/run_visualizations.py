from pathlib import Path
from visualization.phase_map_builder import build_phase_map

Path("reports").mkdir(parents=True, exist_ok=True)
result = build_phase_map()
print("Visualization complete:", result)
