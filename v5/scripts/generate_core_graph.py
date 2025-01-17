import os
import json
import networkx as nx
from networkx.readwrite import json_graph
import shutil

CORE_GRAPH_PATH = "snapshots/core.graph.json"
BACKUP_PATH = "snapshots/core.graph.json.old"

def validate_path(path):
    """Check if a path exists."""
    return os.path.exists(path)

def get_file_metadata(file_path, repo_root):
    """Retrieve basic metadata of a file with a relative path."""
    relative_file_path = relative_path(file_path, repo_root)
    return {
        "type": "file",
        "size": os.path.getsize(file_path),
        "path": relative_file_path
    }

def relative_path(absolute_path, base_path):
    """Get the relative path from base_path to absolute_path."""
    return os.path.relpath(absolute_path, base_path)

def traverse_path(start_path, graph, repo_root):
    """Recursively traverse directories and add nodes/edges for all files."""
    try:
        # Skip hidden directories
        if os.path.basename(start_path).startswith("."):
            print(f"Skipping hidden directory: {start_path}")
            return

        # Process index.json if available
        index_file = os.path.join(start_path, "index.json")
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                index_data = json.load(f)
                print(f"Loaded index.json from {index_file}")
            
            for node in index_data.get("MyShelf", []):
                node_path = os.path.abspath(os.path.join(start_path, node.get("path", "")))
                relative_node_path = relative_path(node_path, repo_root)
                graph.add_node(relative_node_path, **node)  # Add metadata to node
                
                # Add edge between parent and child
                relative_start_path = relative_path(start_path, repo_root)
                graph.add_edge(relative_start_path, relative_node_path)
                print(f"Added edge: {relative_start_path} -> {relative_node_path}")

        # Add all files and directories
        for entry in os.scandir(start_path):
            relative_entry_path = relative_path(entry.path, repo_root)
            
            if entry.is_dir():
                # Skip hidden directories
                if entry.name.startswith("."):
                    print(f"Skipping hidden directory: {entry.path}")
                    continue
                
                # Add directory as a node and recurse
                graph.add_node(relative_entry_path, type="directory", path=relative_entry_path)
                graph.add_edge(relative_path(start_path, repo_root), relative_entry_path)
                traverse_path(entry.path, graph, repo_root)
            elif entry.is_file():
                # Add file as a node with relative path metadata
                metadata = get_file_metadata(entry.path, repo_root)
                graph.add_node(relative_entry_path, **metadata)
                graph.add_edge(relative_path(start_path, repo_root), relative_entry_path)
                print(f"Added file: {relative_entry_path}")

    except Exception as e:
        print(f"Error processing {start_path}: {e}")

def generate_core_graph():
    """Generate the core graph and save it."""
    os.makedirs(os.path.dirname(CORE_GRAPH_PATH), exist_ok=True)

    # Backup existing graph if it exists
    if os.path.exists(CORE_GRAPH_PATH):
        shutil.copy(CORE_GRAPH_PATH, BACKUP_PATH)
        print(f"Backup created: {BACKUP_PATH}")
        os.remove(CORE_GRAPH_PATH)
        print(f"Old core graph deleted: {CORE_GRAPH_PATH}")

    # Initialize a new graph
    graph = nx.DiGraph()
    repo_root = os.getcwd()
    print(f"Starting graph generation from: {repo_root}")

    # Traverse the repository
    traverse_path(repo_root, graph, repo_root)

    if graph.number_of_nodes() == 0:
        print("No nodes found in the graph. Skipping save.")
        return

    # Save the new graph
    graph_data = json_graph.node_link_data(graph)
    with open(CORE_GRAPH_PATH, "w") as f:
        json.dump(graph_data, f, indent=4)

    print(f"Core graph saved to: {CORE_GRAPH_PATH}")
    print(f"Graph nodes: {list(graph.nodes)}")
    print(f"Graph edges: {list(graph.edges)}")

if __name__ == "__main__":
    generate_core_graph()