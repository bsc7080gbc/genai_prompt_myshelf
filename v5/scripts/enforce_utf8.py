import chardet
import sys
import os
import logging

# Set up logging
logging.basicConfig(filename='utf8_validation.log', level=logging.INFO, format='%(asctime)s %(message)s')

def is_utf8(file_path):
    """Check if a file is encoded in UTF-8."""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding'] == 'utf-8'
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return False

def validate_files(file_list):
    """Validate that all files in the list are UTF-8 encoded."""
    all_valid = True
    valid_count = 0
    invalid_count = 0

    for file_path in file_list:
        if not os.path.isfile(file_path):
            print(f"Skipping non-existent file: {file_path}")
            logging.warning(f"Skipping non-existent file: {file_path}")
            continue

        if is_utf8(file_path):
            print(f"UTF-8 compliant: {file_path}")
            logging.info(f"UTF-8 compliant: {file_path}")
            valid_count += 1
        else:
            print(f"Non-UTF-8 file detected: {file_path}")
            logging.warning(f"Non-UTF-8 file detected: {file_path}")
            all_valid = False
            invalid_count += 1

    print(f"\nValidation Summary: {valid_count} valid, {invalid_count} invalid.")
    logging.info(f"Validation Summary: {valid_count} valid, {invalid_count} invalid.")

    if not all_valid:
        sys.exit(1)  # Exit with error code if any file is non-UTF-8

def resolve_paths(file_list, base_dir):
    """Resolve relative paths in file list based on a base directory."""
    return [os.path.join(base_dir, file_path) if not os.path.isabs(file_path) else file_path for file_path in file_list]

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "--filelist":
        print("Usage: python scripts/enforce_utf8.py --filelist <filelist>")
        sys.exit(1)

    filelist_path = sys.argv[2]
    if not os.path.isfile(filelist_path):
        print(f"File list {filelist_path} does not exist.")
        logging.error(f"File list {filelist_path} does not exist.")
        sys.exit(1)

    # Read file list and resolve paths relative to the directory containing filelist_path
    base_dir = os.path.dirname(os.path.abspath(filelist_path))
    with open(filelist_path, 'r') as f:
        files = resolve_paths([line.strip() for line in f.readlines() if line.strip()], base_dir)

    if not files:
        print("No files to validate. Skipping UTF-8 enforcement.")
        logging.info("No files to validate. Skipping UTF-8 enforcement.")
        sys.exit(0)

    validate_files(files)
