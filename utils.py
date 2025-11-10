from graph import Graph
from node import Node
import numpy as np

def create_graph_from_json(json_data):
    """
    Create a Graph object from already-parsed JSON (Python list of dicts).
    """
    graph = Graph()

    for row in json_data:
        source_id = str(row["source"])
        target_id = str(row["target"])
        weight = float(row["weight"])
        bidirectional = bool(row["bidirectional"])

        if source_id not in graph.nodes:
            graph.add_node(Node(source_id, np.inf))
        if target_id not in graph.nodes:
            graph.add_node(Node(target_id, np.inf))

        graph.add_edge(
            graph.nodes[source_id],
            graph.nodes[target_id],
            weight,
            bidirectional
        )

    return graph


def reconstruct_path(prev, start_node, end_node):
    if end_node not in prev and end_node != start_node:
        return None

    path = []
    cur = end_node
    while cur is not None:
        path.append(cur.id)   # Node → string
        cur = prev.get(cur, None)

    path.reverse()

    return path

