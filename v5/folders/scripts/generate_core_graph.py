import os
import json
import shutil
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import mimetypes
import networkx as nx
from networkx.readwrite import json_graph
from collections import Counter

# Constants
CORE_GRAPH_PATH = "snapshots/core.graph.json"
BACKUP_PATH = "snapshots/core.graph.json.old"

# User-configurable parameters
# Read environment variables, defaulting to 10 if not set
KEYWORD_GOAL = int(os.getenv("KEYWORD_GOAL", 10))
KEYWORD_ATTEMPT_THRESHOLD = int(os.getenv("KEYWORD_ATTEMPT_THRESHOLD", 10))

print(f"Using KEYWORD_GOAL={KEYWORD_GOAL} and KEYWORD_ATTEMPT_THRESHOLD={KEYWORD_ATTEMPT_THRESHOLD}")

IGNORE_KEYWORDS = set([
    # Formatting and Numeric Artifacts
    "#", "##", "###", "####", "#####",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
    "20", "21", "22", "23", "24", "25", "30", "40", "50", "60",

    # Time References
    "minutes", "minute", "hour", "hours", "second", "seconds", 
    "day", "month", "year", "today", "yesterday", "tomorrow",
    "timestamp", "duration", "10 minutes", "20 minutes", "30 minutes",
    "6-8 minutes", "8-10 minutes", "10-12 minutes", 
    "10-15 minutes", "10-15 seconds", "2-3 minutes", "3-4 minutes",
    "1-2 hours", "2-3 hours", "3-4 hours", "4-5 hours",

    # Culinary Terms
    "cup", "cups", "tbsp", "tsp", "1 tbsp", "15 ml", "¼ cup", 
    "ingredient", "ingredients", "butter", "garlic", "thyme", 
    "cheddar", "parmesan", "lemon", "cranberry", "pancakes", 
    "chocolate", "8x8-inch", "oven", "food", "oz", "ounces",
    "gallon",

    # Instructions and Procedures
    "instruction", "instructions", "## instructions", 
    "### instructions", "### instructions\n1", "prepare", "add", 
    "repeat", "mix", "heat", "bake", "chill", "serve", "cook", 
    "spread", "pour", "flip",

    # Metadata and Properties
    "metadata", "path", "name", "type", "size", "json", "index", 
    "data", "value", "result", "info", "details", "root", "base", 
    "structure", "file", "directory", "node", "edge", "link", "map", 
    "key", "id", "list", "text", "string", "number", "integer", 
    "float", "binary", "content", "document", "record", "log", 
    "entry", "graph",

    # Status and Process Descriptions
    "validate", "verified", "check", "verify", "not found", "found", 
    "added", "removed", "created", "updated", "new", "old", "latest", 
    "previous", "current", "next", "action", "trigger", "process", 
    "execute", "run", "status", "step", "retry", "attempt", 
    "success", "failure", "error", "warning", "critical",

    # Generic Phrases and Terms
    "personal", "represents", "a rough day", "un", "one", "two", 
    "three", "home", "core", "system", "set", "get", "define", "use", 
    "yes", "no", "true", "false", "on", "off", "first", "second", 
    "third", "fourth", "fifth", "final",

    # Technical and Log Terms
    "debug", "log message", "info", "trace", "utc", "timezone", 
    "offset", "value", "instance", "class", "object", "method", 
    "function", "operation", "statement", "expression", "condition", 
    "loop", "iteration", "array", "dictionary", "tuple", "set", 
    "queue", "stack", "algorithm", "hex", "oct", "decimal", 
    "hexadecimal", "ascii", "unicode", "utf-8",

    # Persona and Mode-Related Terms
    "ai", "llm", 

    # Journal and Context-Specific Words
    "january", "2025", "new year", "goals", 

    # Dewey and Library Context
    "dewey decimal", "dewey"
])

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def validate_path(path):
    return os.path.exists(path)

def relative_path(absolute_path, base_path):
    return os.path.relpath(absolute_path, base_path)

def extract_keywords_from_file(file_path):
    keywords = set()
    attempts = 0
    while len(keywords) < KEYWORD_GOAL and attempts < KEYWORD_ATTEMPT_THRESHOLD:
        attempts += 1
        try:
            mime_type = mimetypes.guess_type(file_path)[0]
            if mime_type and not mime_type.startswith("text"):
                return []
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            doc = nlp(content)
            for ent in doc.ents:
                keywords.add(ent.text.lower())

            vectorizer = TfidfVectorizer(stop_words="english", max_features=KEYWORD_GOAL)
            tfidf_matrix = vectorizer.fit_transform([content])
            keywords.update(map(str.lower, vectorizer.get_feature_names_out()))

            keywords -= IGNORE_KEYWORDS
        except Exception as e:
            print(f"Keyword extraction error for {file_path}: {e}")
            break
    return list(keywords)

def traverse_path(start_path, graph, repo_root):
    """Recursively traverse specific directories and add nodes/edges for valid files."""
    try:
        # Normalize paths
        normalized_repo_root = os.path.abspath(repo_root)
        valid_base_paths = [
            os.path.join(normalized_repo_root, "MyLibrary"),
            os.path.join(normalized_repo_root, "context")
        ]

        if not any(start_path.startswith(base) for base in valid_base_paths):
            print(f"Skipping path outside of allowed directories: {start_path}")
            return

        # Special handling for context: only process context.session.* files
        if "context" in start_path:
            for entry in os.scandir(start_path):
                if entry.is_file() and entry.name.startswith("context.session."):
                    relative_entry_path = relative_path(entry.path, repo_root)
                    metadata = get_file_metadata(entry.path, repo_root)
                    graph.add_node(relative_entry_path, **metadata)
                    graph.add_edge(relative_path(start_path, repo_root), relative_entry_path)
                    print(f"Added context session file: {relative_entry_path} with metadata: {metadata}")
            return  # Do not recurse further into context

        # Traverse directories and process files
        for entry in os.scandir(start_path):
            if entry.name.startswith("."):
                print(f"Skipping hidden entry: {entry.path}")
                continue

            relative_entry_path = relative_path(entry.path, repo_root)

            if entry.is_dir():
                # Recurse into valid directories
                graph.add_node(relative_entry_path, type="directory", path=relative_entry_path)
                graph.add_edge(relative_path(start_path, repo_root), relative_entry_path)
                traverse_path(entry.path, graph, repo_root)
            elif entry.is_file():
                # Add valid files
                metadata = get_file_metadata(entry.path, repo_root)
                graph.add_node(relative_entry_path, **metadata)
                graph.add_edge(relative_path(start_path, repo_root), relative_entry_path)
                print(f"Added file: {relative_entry_path} with metadata: {metadata}")
    except Exception as e:
        print(f"Error processing {start_path}: {e}")


def get_file_metadata(file_path, repo_root):
    relative_file_path = relative_path(file_path, repo_root)
    metadata = {
        "type": "file",
        "size": os.path.getsize(file_path),
        "path": relative_file_path,
        "keywords": extract_keywords_from_file(file_path)
    }
    return metadata

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

    # Traverse only valid paths
    for valid_path in ["MyLibrary", "context"]:
        traverse_path(os.path.join(repo_root, valid_path), graph, repo_root)

    if graph.number_of_nodes() == 0:
        print("No nodes found in the graph. Skipping save.")
        return

    # Save the new graph
    graph_data = json_graph.node_link_data(graph)
    with open(CORE_GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=4)

    print(f"Core graph saved to: {CORE_GRAPH_PATH}")
    print(f"Graph nodes: {list(graph.nodes)}")
    print(f"Graph edges: {list(graph.edges)}")


if __name__ == "__main__":
    generate_core_graph()

