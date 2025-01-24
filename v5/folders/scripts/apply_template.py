import json
import sys
import os
import logging

# Set script directory as the working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, ".."))
os.chdir(root_dir)

# Update log file path to reflect the root directory
logging.basicConfig(filename='workflow.log', level=logging.INFO, format='%(asctime)s %(message)s')

DRYRUN = os.getenv('DRYRUN', 'false').lower() == 'true'

def deep_merge(target, source):
    """Recursively merge two dictionaries, excluding schema-related fields."""
    schema_keys = {"type", "properties", "required", "additionalProperties", "patternProperties"}
    for key, value in source.items():
        if key in schema_keys:
            continue  # Skip schema-specific fields
        if key == "Metadata" and "Description" in value:
            target[key]["Description"] = target[key].get("Description", value["Description"])
        elif isinstance(value, dict) and key in target and isinstance(target[key], dict):
            deep_merge(target[key], value)
        else:
            target[key] = value

def apply_template(data_path, template_path):
    """Apply template to data.json."""
    try:
        # Load data.json and template.json
        with open(data_path, 'r') as f:
            data = json.load(f)
        with open(template_path, 'r') as t:
            template = json.load(t)

        # Backup existing data.json
        if not DRYRUN and os.path.exists(data_path):
            backup_path = f"{data_path}.bak"
            os.rename(data_path, backup_path)
            logging.info(f"Backup created: {backup_path}")

        # Merge template into data
        deep_merge(data, template)

        # Save changes in DRYRUN or normal mode
        output_path = f"{data_path}.tmp" if DRYRUN else data_path
        with open(output_path, 'w') as out:
            json.dump(data, out, indent=4)
        logging.info(f"Template applied {'(DRYRUN)' if DRYRUN else ''} successfully to {output_path}.")
        print(f"Template applied {'(DRYRUN)' if DRYRUN else ''} successfully.")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        print(f"Error decoding JSON: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        print(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Adjust paths to be relative to the root directory
    apply_template('updates/data.json', 'template.json')
