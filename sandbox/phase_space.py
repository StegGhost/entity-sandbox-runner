from __future__ import annotations

from pathlib import Path
import json

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _ensure_visuals_dir(results_path: Path) -> Path:
    visuals_dir = results_path.parent / "visuals"
    visuals_dir.mkdir(parents=True, exist_ok=True)
    return visuals_dir


def _compute_rows(result: dict) -> list[dict]:
    rows = []
    receipts = result.get("receipts", [])
    for receipt in receipts:
        proposal = receipt.get("proposal", {})
        g = proposal.get("g_next")
        c = proposal.get("c_next")
        t = proposal.get("t_next")
        a = proposal.get("a_next")

        K = proposal.get("K", 1.0)
        alpha = proposal.get("alpha", 1.0)
        beta = proposal.get("beta", 1.0)
        gamma = proposal.get("gamma", 1.0)

        if g is None or c is None or t is None or a is None:
            continue

        bound = K * (g ** alpha) * (c ** beta) * (t ** gamma)
        rows.append(
            {
                "step": receipt.get("step"),
                "a_next": a,
                "g_next": g,
                "c_next": c,
                "t_next": t,
                "bound": bound,
                "admissible": bool(receipt.get("admissible")),
            }
        )
    return rows


def _plot_pressure_vs_bound(rows: list[dict], outpath: Path) -> bool:
    if plt is None or not rows:
        return False

    steps = [r["step"] for r in rows]
    pressure = [r["a_next"] for r in rows]
    bound = [r["bound"] for r in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(steps, pressure, label="artifact pressure")
    plt.plot(steps, bound, label="admissibility bound")
    plt.xlabel("step")
    plt.ylabel("value")
    plt.title("GCAT pressure vs admissibility bound")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()
    return True


def _plot_g_t_phase_space(rows: list[dict], outpath: Path) -> bool:
    if plt is None or not rows:
        return False

    g_values = [r["g_next"] for r in rows]
    t_values = [r["t_next"] for r in rows]

    plt.figure(figsize=(6, 6))
    plt.plot(g_values, t_values, marker="o")
    plt.xlabel("g_next")
    plt.ylabel("t_next")
    plt.title("GCAT phase space: governance vs trust")
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()
    return True


def build_phase_space_visuals(results_path: Path) -> dict:
    result = _load_json(results_path)
    visuals_dir = _ensure_visuals_dir(results_path)
    rows = _compute_rows(result)

    experiment = result.get("experiment", results_path.stem)
    generated_files = []

    pressure_chart = visuals_dir / f"{experiment}_pressure_vs_bound.png"
    if _plot_pressure_vs_bound(rows, pressure_chart):
        generated_files.append(pressure_chart.name)

    phase_chart = visuals_dir / f"{experiment}_g_t_phase_space.png"
    if _plot_g_t_phase_space(rows, phase_chart):
        generated_files.append(phase_chart.name)

    summary = {
        "visualization_version": "1.0",
        "experiment": experiment,
        "results_file": str(results_path.name),
        "matplotlib_available": plt is not None,
        "row_count": len(rows),
        "generated_files": generated_files,
    }

    manifest_path = visuals_dir / f"{experiment}_visualization_manifest.json"
    manifest_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md_lines = [
        f"# Visualization Summary: {experiment}",
        "",
        f"- Matplotlib available: `{summary['matplotlib_available']}`",
        f"- Data rows: `{summary['row_count']}`",
        "",
        "## Generated Files",
        "",
    ]
    if generated_files:
        for name in generated_files:
            md_lines.append(f"- `{name}`")
    else:
        md_lines.append("- none")

    (visuals_dir / f"{experiment}_visualization_summary.md").write_text(
        "\n".join(md_lines) + "\n",
        encoding="utf-8",
    )

    return summary