import json
from fastapi import UploadFile
from graph import Graph
from node import Node
import numpy as np


def create_graph_from_json(file: UploadFile):
    """
    Create a Graph object from the uploaded JSON file.

    Expected JSON format:
    [
        {"source": "A", "target": "B", "weight": 3, "bidirectional": true},
        ...
    ]
    """
    # Load JSON content
    data = json.loads(file.file.read())

    graph = Graph()

    # Add nodes and edges
    for row in data:
        source_id = str(row["source"])
        target_id = str(row["target"])
        weight = float(row["weight"])
        bidirectional = bool(row["bidirectional"])

        # Add nodes if they do not exist
        if source_id not in graph.nodes:
            graph.add_node(Node(source_id, np.inf))
        if target_id not in graph.nodes:
            graph.add_node(Node(target_id, np.inf))

        # Add edge
        graph.add_edge(
            graph.nodes[source_id],
            graph.nodes[target_id],
            weight,
            bidirectional
        )

    return graph


def reconstruct_path(prev, start, end):
    """
    Reconstruct the shortest path from the predecessor dictionary returned by Dijkstra.

    Args:
        prev (dict): map of {node_id: previous_node_id}
        start (str): starting node id
        end (str): ending node id

    Returns:
        list[str] or None: the reconstructed path
    """
    # Path impossible if end was never reached
    if end not in prev:
        return None

    path = []
    current = end

    # Trace backwards from end → start
    while current is not None:
        path.append(current)
        current = prev[current]

    path.reverse()

    # Validate reachability
    if path[0] != start:
        return None

    return path
