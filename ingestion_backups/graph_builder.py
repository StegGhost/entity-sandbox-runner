import networkx as nx
_graph = nx.DiGraph()

def add_entity(entity_id: str):
    _graph.add_node(entity_id)

def add_interaction(source: str, target: str, weight: float = 1.0):
    _graph.add_edge(source, target, weight=weight)

def get_graph():
    return _graph
