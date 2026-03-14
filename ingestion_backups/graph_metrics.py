import networkx as nx
from interaction_graph.graph_builder import get_graph

def compute_metrics():
    g = get_graph()
    return {
        "nodes": len(g.nodes),
        "edges": len(g.edges),
        "density": 0.0 if len(g.nodes) == 0 else nx.density(g),
    }
