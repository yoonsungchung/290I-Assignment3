from fastapi import FastAPI, UploadFile, File
import json
from utils import create_graph_from_json, reconstruct_path
from dijkstra import dijkstra

app = FastAPI()

active_graph = None


@app.get("/")
async def root():
    return {"message": "Welcome to the Shortest Path Solver!"}


@app.post("/upload_graph_json/")
async def upload_graph_json(file: UploadFile = File(...)):
    global active_graph

    if not file.filename.endswith(".json"):
        return {"Upload Error": "Invalid file type. Please upload a JSON file."}

    try:
        raw = await file.read()
        parsed_json = json.loads(raw.decode("utf-8"))

        # send parsed JSON list to utils
        active_graph = create_graph_from_json(parsed_json)

        return {"Upload Success": file.filename}

    except Exception as e:
        return {"Upload Error": str(e)}


@app.get("/solve_shortest_path/")
async def solve_shortest_path(start_node_id: str, end_node_id: str):
    global active_graph

    if active_graph is None:
        return {"Solver Error": "No active graph, please upload a graph first."}

    # node
    if start_node_id not in active_graph.nodes or end_node_id not in active_graph.nodes:
        return {"Solver Error": "Invalid start or end node ID."}

    start_node = active_graph.nodes[start_node_id]
    end_node = active_graph.nodes[end_node_id]

    try:
        # run Dijkstra (updates nodes in place)
        dijkstra(active_graph, start_node)

        # reconstruct path
        path = []
        cur = end_node
        while cur is not None:
            path.append(cur.id)
            cur = cur.prev
        path.reverse()

        if path[0] != start_node_id:
            return {"Solver Error": "No path found between nodes."}

        total_distance = end_node.dist

    except Exception as e:
        return {"Solver Error": f"Internal solver failure: {str(e)}"}

    return {
        "shortest_path": path,
        "total_distance": total_distance
    }
