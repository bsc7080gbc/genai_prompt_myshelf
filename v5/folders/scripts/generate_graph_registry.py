import json
import os

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, ".."))
MINI_GRAPHS_DIR = os.path.join(root_dir, "snapshots/mini-graphs")
REGISTRY_PATH = os.path.join(root_dir, "snapshots/mini-graphs/registry.json")
MYLIBRARY_DIR = os.path.join(root_dir, "MyLibrary")

def load_existing_registry(path):
    """Load the existing registry if it exists."""
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading existing registry: {e}")
    return {}

def extract_metadata_from_index(index_path):
    """Extract keywords and description from an index.json file."""
    if not os.path.exists(index_path):
        print(f"Index file not found at: {index_path}. Using defaults.")
        return [], "No description available."

    try:
        with open(index_path, 'r', encoding="utf-8") as f:
            index_data = json.load(f)
            keywords = index_data.get("keywords", [])
            description = index_data.get("description", "No description available.")
            return keywords, description
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading index.json at {index_path}: {e}. Using defaults.")
        return [], "No description available."

def graph_id_to_index_path(graph_id, base_dir):
    """Convert a graph ID to its corresponding index.json path."""
    original_path = graph_id.replace("_", "/")
    index_path = os.path.join(base_dir, original_path, "index.json")
    return index_path

def merge_registry(existing_registry, new_registry):
    """Merge new registry entries with the existing registry."""
    merged_registry = existing_registry.copy()
    for graph_id, data in new_registry.items():
        if graph_id in merged_registry:
            # Update keywords and description only if new data is meaningful
            merged_registry[graph_id]["keywords"] = data["keywords"] or merged_registry[graph_id].get("keywords", [])
            merged_registry[graph_id]["description"] = data["description"] or merged_registry[graph_id].get("description", "No description available.")
        else:
            # Add new entry if it doesn't exist
            merged_registry[graph_id] = data
    return merged_registry

def generate_registry(mini_graphs_dir, library_dir):
    """Generate a registry mapping all mini-graphs to their domains."""
    new_registry = {}
    skipped_files = []

    for root, _, files in os.walk(mini_graphs_dir):
        for file in files:
            if file.endswith(".graph.json"):
                mini_graph_path = os.path.join(root, file)
                try:
                    graph_id = file.replace(".graph.json", "").replace("_", "/")
                    relative_path = os.path.relpath(mini_graph_path, root_dir)

                    # Find the corresponding index.json
                    index_path = graph_id_to_index_path(graph_id, library_dir)
                    keywords, description = extract_metadata_from_index(index_path)

                    if not keywords:
                        print(f"No keywords found for graph ID: {graph_id}")
                    if description == "No description available.":
                        print(f"No description available for graph ID: {graph_id}")

                    # Add to registry
                    new_registry[graph_id] = {
                        "path": relative_path,
                        "keywords": keywords,
                        "description": description,
                    }
                except Exception as e:
                    skipped_files.append(mini_graph_path)
                    print(f"Skipping file due to error: {e}. File: {mini_graph_path}")

    if skipped_files:
        print(f"Skipped {len(skipped_files)} files due to errors:")
        for skipped_file in skipped_files:
            print(f" - {skipped_file}")

    return new_registry

if __name__ == "__main__":
    print("Generating registry...")
    existing_registry = load_existing_registry(REGISTRY_PATH)
    new_registry = generate_registry(MINI_GRAPHS_DIR, MYLIBRARY_DIR)
    merged_registry = merge_registry(existing_registry, new_registry)

    # Save the merged registry
    with open(REGISTRY_PATH, 'w', encoding="utf-8") as f:
        json.dump(merged_registry, f, indent=4)
    print(f"Registry saved to {REGISTRY_PATH}")
