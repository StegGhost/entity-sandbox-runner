from pathlib import Path
import json
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

def build_phase_space_visuals(results_path: Path) -> dict:
    visuals_dir = Path("reports/visuals")
    visuals_dir.mkdir(parents=True, exist_ok=True)

    result = json.loads(results_path.read_text(encoding="utf-8"))
    rows = result.get("trajectory", [])
    experiment = result.get("experiment", results_path.stem)
    generated = []

    if plt is not None and rows:
        steps = [r["step"] for r in rows]
        pressure = [r["a_next"] for r in rows]
        bound = [r["bound"] for r in rows]
        plt.figure(figsize=(8, 5))
        plt.plot(steps, pressure, label="artifact pressure")
        plt.plot(steps, bound, label="admissibility bound")
        plt.xlabel("step")
        plt.ylabel("value")
        plt.title("Pressure vs Bound")
        plt.legend()
        out = visuals_dir / f"{experiment}_pressure_vs_bound.png"
        plt.tight_layout()
        plt.savefig(out, dpi=160)
        plt.close()
        generated.append(out.name)

    manifest = {
        "experiment": experiment,
        "generated_files": generated,
        "matplotlib_available": plt is not None,
    }
    (visuals_dir / f"{experiment}_visualization_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest
