import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Load spaCy model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# Define paths
CORE_GRAPH_PATH = "snapshots/core.graph.json"
OUTPUT_DIR = "snapshots/mini-graphs"
REGISTRY_PATH = "snapshots/mini-graphs/registry.json"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_core_graph(path):
    """Load the core graph JSON file."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def reverse_and_format_path(path):
    """Reverse the path, truncate 'MyLibrary', and format the name."""
    segments = path.split("/")
    if "MyLibrary" in segments:
        segments.remove("MyLibrary")
    reversed_segments = segments[::-1]
    return "_".join(reversed_segments) + ".graph.json"

def extract_file_content(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except (UnicodeDecodeError, FileNotFoundError) as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def extract_keywords_and_description(texts):
    """Extract keywords and a summary description from a list of texts."""
    combined_text = " ".join(texts).strip()  # Combine texts and remove extra whitespace
    if not combined_text:
        print("No valid text for keyword extraction.")
        return [], "No description available."

    try:
        doc = nlp(combined_text)
        key_phrases = {chunk.text for chunk in doc.noun_chunks}

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([combined_text])  # Ensure non-empty input
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray().flatten()))
        high_value_phrases = {phrase for phrase in key_phrases if tfidf_scores.get(phrase.lower(), 0) > 0.1}

        sentences = list(doc.sents)
        summary = sentences[0].text if sentences else "No description available."
        return list(high_value_phrases), summary

    except ValueError as e:
        print(f"Keyword extraction failed: {e}")
        return [], "No description available."

def split_by_directories(core_graph):
    """Split the core graph dynamically based on 'type: directory' entries."""
    directories = [node for node in core_graph.get("nodes", []) if node.get("type") == "directory"]
    edges = core_graph.get("edges", [])

    active_files = []  # Track active mini-graphs for this run
    registry = {}  # Registry for mini-graphs

    for directory in directories:
        dir_id = directory.get("id")
        dir_path = directory.get("path")

        # Filter nodes belonging to this directory
        filtered_nodes = [
            node for node in core_graph.get("nodes", [])
            if node.get("path", "").startswith(dir_path)
        ]

        # Find edges connected to these nodes
        node_ids = {node["id"] for node in filtered_nodes}
        filtered_edges = [
            edge for edge in edges
            if edge["source"] in node_ids or edge["target"] in node_ids
        ]

        # Extract keywords and description for each file in the directory
        file_texts = []
        file_keywords = []
        for node in filtered_nodes:
            if node.get("type") == "file":
                file_content = extract_file_content(node["path"])
                if file_content:
                    file_texts.append(file_content)
                    keywords, _ = extract_keywords_and_description([file_content])
                    node["keywords"] = keywords  # Add keywords to file node
                    file_keywords.extend(keywords)

        # Aggregate keywords and description for the mini-graph
        keywords, description = extract_keywords_and_description(file_texts)

        # Construct the mini-graph
        mini_graph = {
            "type": "mini-graph",
            "id": dir_id,
            "nodes": filtered_nodes,
            "edges": filtered_edges,
            "keywords": keywords,  # Include aggregated keywords
            "description": description,  # Include aggregated description
        }

        # Generate the output file name
        output_file_name = reverse_and_format_path(dir_path)
        output_path = os.path.join(OUTPUT_DIR, output_file_name)

        # Save the mini-graph
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(mini_graph, file, indent=4)
        print(f"Saved mini-graph for directory '{dir_path}' to {output_path}")

        # Add to registry
        registry[dir_path] = {
            "path": output_path,
            "keywords": keywords,
            "description": description,
        }

        # Track the active file
        active_files.append(output_file_name)

    return active_files, registry

def save_registry(registry, registry_path):
    """Save the registry to a JSON file."""
    with open(registry_path, "w", encoding="utf-8") as file:
        json.dump(registry, file, indent=4)
    print(f"Saved registry to {registry_path}")

def main():
    """Main script function."""
    print("Loading core graph...")
    core_graph = load_core_graph(CORE_GRAPH_PATH)

    print("Splitting core graph into mini-graphs by directory...")
    active_files, registry = split_by_directories(core_graph)

    print("Saving registry...")
    save_registry(registry, REGISTRY_PATH)

    print("Mini-graphs generated and registry updated successfully!")

if __name__ == "__main__":
    main()
