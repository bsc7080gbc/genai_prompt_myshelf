import json
import sys
import logging
import os
from jsonschema import validate, ValidationError

# Set script directory as the working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, ".."))
os.chdir(root_dir)

# Update log file path to reflect the root directory
logging.basicConfig(filename='workflow.log', level=logging.INFO, format='%(asctime)s %(message)s')

def validate_json_syntax(file_path):
    """Validate JSON file syntax."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logging.info(f"Syntax validation passed for {file_path}.")
        print(f"Syntax validation passed for {file_path}.")
        return data
    except json.JSONDecodeError as e:
        logging.error(f"JSON syntax validation failed for {file_path}: {e}")
        print(f"JSON syntax validation failed for {file_path}: {e}")
        return None
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}")
        print(f"File not found: {file_path}")
        return None

def validate_json_structure(data, schema_path):
    """Validate JSON data against a schema."""
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        validate(instance=data, schema=schema)
        logging.info("Structure validation passed against schema.")
        print("Structure validation passed against schema.")
        return True
    except ValidationError as e:
        logging.error(f"Schema validation failed: {e}")
        print(f"Schema validation failed: {e}")
        return False
    except FileNotFoundError as e:
        logging.error(f"Schema file not found: {schema_path}")
        print(f"Schema file not found: {schema_path}")
        return False

if __name__ == "__main__":
    # Paths are now relative to the root directory
    data_file = 'updates/data.json'
    schema_file = 'schema.json'

    # Validate syntax
    json_data = validate_json_syntax(data_file)
    if json_data is None:
        sys.exit(1)

    # Validate structure
    if not validate_json_structure(json_data, schema_file):
        sys.exit(1)
