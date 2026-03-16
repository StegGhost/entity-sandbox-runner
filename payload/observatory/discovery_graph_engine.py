import json
from pathlib import Path

try:
    from observatory.pipeline_contract import pipeline_contract
except Exception:
    def pipeline_contract(**kwargs):
        def decorator(func):
            return func
        return decorator

@pipeline_contract(
    name="discovery_graph_engine",
    tier=4,
    order=940,
    inputs=["observatory/symbolic_regression_results.json"],
    outputs=["observatory/discovery_graph.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    input_path = Path("observatory/symbolic_regression_results.json")
    output_path = Path("observatory/discovery_graph.json")

    if input_path.exists():
        try:
            data = json.loads(input_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    else:
        data = {}

    nodes = []
    edges = []
    for item in data.get("candidate_equations", []):
        eq = item.get("equation")
        if not eq:
            continue
        nodes.append({"id": eq, "type": "equation", "score": item.get("score")})
        edges.append({"source": "phase_space", "target": eq, "relation": "suggests"})

    graph = {"nodes": [{"id": "phase_space", "type": "dataset"}] + nodes, "edges": edges}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    print(json.dumps({"nodes": len(graph["nodes"]), "edges": len(graph["edges"])}, indent=2))


if __name__ == "__main__":
    main()
