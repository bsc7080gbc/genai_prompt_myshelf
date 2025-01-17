def backup_theme_registry():
    """Back up the existing theme registry."""
    if os.path.exists(THEME_REGISTRY_PATH):
        backup_path = THEME_REGISTRY_PATH.replace(".json", ".old.json")
        shutil.copyfile(THEME_REGISTRY_PATH, backup_path)
        log.info(f"Backed up existing theme registry to {backup_path}")

def create_theme_registry():
    """Create a registry for thematic mini-graphs with related mini-graphs."""
    backup_theme_registry()  # Backup before creating a new registry

    mini_graph_registry = load_registry(REGISTRY_PATH)
    theme_registry = []
    
    for file in os.listdir(THEMATIC_MINI_GRAPHS_DIR):
        if file.endswith(".theme.graph.json"):
            theme_name = file.replace(".theme.graph.json", "")
            theme_file_path = os.path.join(THEMATIC_MINI_GRAPHS_DIR, file)

            # Load the theme's graph to get its keywords
            with open(theme_file_path, "r", encoding="utf-8") as f:
                theme_graph = json.load(f)
                theme_keywords = theme_graph.get("graph", {}).get("keywords", [])

            # Compare theme keywords against all mini-graphs in the registry
            related_mini_graphs = []
            for graph_id, graph_data in mini_graph_registry.items():
                weighting = calculate_weighting(theme_keywords, graph_data)
                if weighting >= WEIGHT_THRESHOLD:
                    related_mini_graphs.append({
                        "path": graph_data["path"],
                        "keywords": graph_data["keywords"],
                        "description": graph_data["description"],
                        "weighting": round(weighting, 2),
                    })

            # Sort related graphs by weighting (highest first)
            related_mini_graphs.sort(key=lambda x: x["weighting"], reverse=True)

            # Add to theme registry
            theme_registry.append({
                "theme": theme_name,
                "path": theme_file_path,
                "keywords": theme_keywords,
                "related_mini_graphs": related_mini_graphs,
            })

    # Save the updated theme registry
    with open(THEME_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(theme_registry, f, indent=4)
    log.info(f"Theme registry created at {THEME_REGISTRY_PATH}")

