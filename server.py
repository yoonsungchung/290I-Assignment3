from fastapi import FastAPI, UploadFile, File
from utils import create_graph_from_json, reconstruct_path
from dijkstra import dijkstra

app = FastAPI()

# Store uploaded graph
active_graph = None


@app.get("/")
async def root():
    return {"message": "Welcome to the Shortest Path Solver!"}


@app.post("/upload_graph_json/")
async def upload_graph_json(file: UploadFile = File(...)):
    """Upload JSON graph file and convert it to Graph object."""
    global active_graph

    # Validate file type
    if not file.filename.endswith(".json"):
        return {"Upload Error": "File must be a JSON"}

    try:
        # Use the JSON-to-Graph builder from utils.py
        active_graph = create_graph_from_json(file)
        return {"Upload Success": file.filename}

    except Exception as e:
        return {"Upload Error": str(e)}


@app.get("/solve_shortest_path/start_node_id={start_node_id}&end_node_id={end_node_id}")
async def solve_shortest_path(start_node_id: str, end_node_id: str):
    """Solves the shortest path using Dijkstra."""
    global active_graph

    if active_graph is None:
        return {"Solver Error": "Please upload a graph first."}

    if start_node_id not in active_graph.nodes or end_node_id not in active_graph.nodes:
        return {"Solver Error": "Invalid start or end node ID."}

    # Run the Dijkstra algorithm
    dist, prev = dijkstra(active_graph, start_node_id)

    path = reconstruct_path(prev, start_node_id, end_node_id)
    if path is None:
        return {"Solver Error": "No path exists between the selected nodes."}

    return {
        "shortest_path": path,
        "total_distance": dist[end_node_id]
    }
