import os
import json
import networkx as nx
from networkx.readwrite import json_graph

# Paths
CORE_GRAPH_PATH = "snapshots/core.graph.json"
MINI_GRAPHS_DIR = "snapshots/mini-graphs"

def load_core_graph():
    """Load the core graph data from the JSON file."""
    if not os.path.exists(CORE_GRAPH_PATH):
        raise FileNotFoundError(f"Core graph not found at {CORE_GRAPH_PATH}")
    
    with open(CORE_GRAPH_PATH, "r", encoding="utf-8") as f:
        return json_graph.node_link_graph(json.load(f))

def extract_subgraph(core_graph, node_id):
    """Extract a subgraph starting from a specific node ID."""
    if node_id not in core_graph:
        print(f"Node {node_id} not found in the core graph. Skipping.")
        return None

    subgraph_nodes = nx.descendants(core_graph, node_id) | {node_id}
    return core_graph.subgraph(subgraph_nodes).copy()

def save_subgraph(subgraph, graph_id):
    """Save a subgraph to a file."""
    subgraph_path = os.path.join(MINI_GRAPHS_DIR, f"{graph_id.replace('/', '_')}.graph.json")
    os.makedirs(os.path.dirname(subgraph_path), exist_ok=True)

    # Prepare node-link data for JSON serialization
    subgraph_data = json_graph.node_link_data(subgraph)

    # Save the subgraph data to the file
    with open(subgraph_path, "w", encoding="utf-8") as f:
        json.dump(subgraph_data, f, indent=4)
    print(f"Mini-graph saved to {subgraph_path}")

def process_node(core_graph, node_id):
    """Process a single node to create its mini-graph."""
    subgraph = extract_subgraph(core_graph, node_id)
    if subgraph:
        # Normalize keywords to lowercase
        for node in subgraph.nodes(data=True):
            if "keywords" in node[1]:
                node[1]["keywords"] = list(set(kw.lower() for kw in node[1]["keywords"]))
        save_subgraph(subgraph, node_id)

def generate_mini_graphs():
    """Generate mini-graphs for each node in the core graph."""
    core_graph = load_core_graph()
    os.makedirs(MINI_GRAPHS_DIR, exist_ok=True)

    for node_id in core_graph.nodes:
        print(f"Processing node: {node_id}")
        process_node(core_graph, node_id)

if __name__ == "__main__":
    generate_mini_graphs()
