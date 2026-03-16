import json
from pathlib import Path
from observatory.pipeline_contract import pipeline_contract

INPUT = Path("federation_plane/nodes.json")
OUTPUT = Path("observatory/federated_node_auth_registry.json")


@pipeline_contract(
    name="federated_node_auth_registry",
    order=472,
    tier=4,
    inputs=["federation_plane/nodes.json"],
    outputs=["observatory/federated_node_auth_registry.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    nodes = []
    if INPUT.exists():
        try:
            nodes = json.loads(INPUT.read_text(encoding="utf-8"))
        except Exception:
            nodes = []
    payload = {
        "node_count": len(nodes),
        "nodes": [
            {"url": n if isinstance(n, str) else n.get("url"), "trusted": True}
            for n in nodes
        ],
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"node_count": len(nodes)}, indent=2))


if __name__ == "__main__":
    main()
