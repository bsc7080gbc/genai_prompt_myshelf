import os
import json
import networkx as nx
from networkx.readwrite import json_graph

CORE_GRAPH_PATH = "snapshots/core.graph.json"
MINI_GRAPHS_DIR = "snapshots/mini-graphs"

def load_core_graph():
    with open(CORE_GRAPH_PATH, "r", encoding="utf-8") as f:
        return json_graph.node_link_graph(json.load(f))

def generate_mini_graphs():
    os.makedirs(MINI_GRAPHS_DIR, exist_ok=True)
    core_graph = load_core_graph()
    processed_subgraphs = set()
    for node, data in core_graph.nodes(data=True):
        if data.get("type") == "directory" and node not in processed_subgraphs:
            subgraph = core_graph.subgraph(nx.descendants(core_graph, node) | {node})
            mini_graph_path = os.path.join(
                MINI_GRAPHS_DIR, node.replace("/", "_") + ".graph.json"
            )
            mini_graph_data = json_graph.node_link_data(subgraph)
            for subnode in mini_graph_data["nodes"]:
                subnode["keywords"] = list(
                    {k.lower() for k in subnode.get("keywords", [])}
                )
            with open(mini_graph_path, "w", encoding="utf-8") as f:
                json.dump(mini_graph_data, f, indent=4)
            processed_subgraphs.add(node)
            print(f"Mini-graph created for: {node}")

if __name__ == "__main__":
    generate_mini_graphs()
