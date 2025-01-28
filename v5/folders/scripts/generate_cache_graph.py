import os
import json
import shutil
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

# Constants and Environment Variables
CORE_GRAPH_PATH = "snapshots/core.graph.json"
THEME_REGISTRY_PATH = "snapshots/mini-graph-themes/theme.registry.json"
THEME_GRAPH_DIR = "snapshots/mini-graph-themes"
CONTEXT_DIR = "context"
MINI_GRAPH_DIR = "snapshots/mini-graphs"
INDEX_PATH = os.path.join(THEME_GRAPH_DIR, "index.json")
THEME_MINI_GRAPH_WEIGHT_THRESHOLD = float(os.getenv("THEME_MINI_GRAPH_WEIGHT_THRESHOLD", "0.00"))

# User-configurable parameters
KEYWORD_GOAL = int(os.getenv("KEYWORD_GOAL", 10))
KEYWORD_ATTEMPT_THRESHOLD = int(os.getenv("KEYWORD_ATTEMPT_THRESHOLD", 10))


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


# Initialize SpaCy
nlp = spacy.load("en_core_web_sm")


def load_keywords_from_core(core_path):
    """Extract keywords from core.graph.json."""
    with open(core_path, "r", encoding="utf-8") as f:
        core_graph = json.load(f)

    keywords = set()
    for node in core_graph.get("nodes", []):
        # Add "name" and "keywords" from nodes
        node_keywords = node.get("keywords", [])
        keywords.update(k.lower() for k in node_keywords)
    return keywords

def extract_keywords_with_spacy(content):
    """Extract keywords from text using SpaCy."""
    doc = nlp(content)
    keywords = set()
    for token in doc:
        if token.is_stop or token.is_punct or token.text.lower() in IGNORE_KEYWORDS:
            continue
        if token.pos_ in {"NOUN", "PROPN", "VERB"}:
            keywords.add(token.text.lower())
    for ent in doc.ents:
        keywords.add(ent.text.lower())
    return keywords

def load_context_files(context_dir):
    """Load context session files and extract themes."""
    themes = defaultdict(list)
    for root, _, files in os.walk(context_dir):
        for file in files:
            if file.startswith("context.session.") and file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    keywords = extract_keywords_with_spacy(content) - IGNORE_KEYWORDS
                    for keyword in keywords:
                        themes[keyword].append(file_path)
                except UnicodeDecodeError:
                    print(f"Skipping non-UTF-8 file: {file_path}")
    return themes

def match_themes_to_mini_graphs(themes, mini_graph_dir):
    """Match themes to mini-graphs and calculate weight."""
    theme_to_graphs = defaultdict(dict)
    for mini_graph in os.listdir(mini_graph_dir):
        if mini_graph.endswith(".graph.json") and not mini_graph.startswith("context"):
            mini_graph_path = os.path.join(mini_graph_dir, mini_graph)
            with open(mini_graph_path, "r", encoding="utf-8") as f:
                graph_data = json.load(f)
                mini_graph_keywords = {
                    keyword.lower() for node in graph_data.get("nodes", []) for keyword in node.get("keywords", [])
                }
                for theme, files in themes.items():
                    match_count = len(mini_graph_keywords & {theme})
                    total_keywords = len(mini_graph_keywords) or 1
                    weight = match_count / total_keywords
                    if weight >= THEME_MINI_GRAPH_WEIGHT_THRESHOLD:
                        theme_to_graphs[theme][mini_graph] = round(weight, 2)
    return theme_to_graphs

def generate_theme_registry(themes, theme_to_graphs, registry_path):
    """Generate the theme registry mapping themes to mini-graphs."""
    registry = {}
    for theme, files in themes.items():
        mini_graphs = [
            {"name": graph, "weight": weight}
            for graph, weight in sorted(theme_to_graphs.get(theme, {}).items(), key=lambda x: -x[1])
            if weight > 0.0
        ]
        if mini_graphs:  # Only add themes with meaningful relationships
            registry[theme] = {
                "files": files,
                "mini-graphs": mini_graphs,
            }
    if not registry:
        print("Error: Theme registry is empty. Check the keyword matching logic.")
        if os.listdir(CONTEXT_DIR):  # Ensure context files exist
            raise ValueError("Theme registry is empty despite available context files. Job failed.")
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
    print(f"Saved theme registry to {registry_path}")

def remove_temporary_files():
    """Remove temporary *.theme.graph.json files."""
    for root, _, files in os.walk(THEME_GRAPH_DIR):
        for file in files:
            if file.endswith(".theme.graph.json"):
                os.remove(os.path.join(root, file))
                print(f"Removed temporary file: {file}")

def create_index_copy():
    """Copy theme.registry.json to index.json."""
    if os.path.exists(THEME_REGISTRY_PATH):
        shutil.copyfile(THEME_REGISTRY_PATH, INDEX_PATH)
        print(f"Copied theme registry to index.json: {INDEX_PATH}")

if __name__ == "__main__":
    print("Generating thematic registry...")
    themes = load_context_files(CONTEXT_DIR)
    print(f"Extracted themes from context files: {list(themes.keys())}")
    core_keywords = load_keywords_from_core(CORE_GRAPH_PATH)
    print(f"Core keywords from core graph: {list(core_keywords)}")
    themes = {k: v for k, v in themes.items() if k in core_keywords}
    print(f"Filtered themes matching core keywords: {list(themes.keys())}")
    theme_to_graphs = match_themes_to_mini_graphs(themes, MINI_GRAPH_DIR)
    generate_theme_registry(themes, theme_to_graphs, THEME_REGISTRY_PATH)
    remove_temporary_files()
    create_index_copy()

