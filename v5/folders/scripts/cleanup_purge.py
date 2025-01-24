import os
import re
from datetime import datetime, timedelta

# Load environment variables
DRYRUN = os.getenv("DRYRUN", "false").lower() == "true"
CLEANUP_PERIOD = int(os.getenv("CLEANUP_PERIOD", "10"))  # Default: 10 days

# Define paths relative to the new scripts directory
ARCHIVE_DIR = "../archive"
UPDATES_DATA_JSON = "../updates/data.json"

def extract_date_from_filename(filename):
    """Extract date from the filename based on known patterns."""
    date_patterns = [r"(\d{4}-\d{2}-\d{2})", r"(\d{8})"]
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            date_str = match.group(1)
            try:
                if "-" in date_str:
                    return datetime.strptime(date_str, "%Y-%m-%d")
                else:
                    return datetime.strptime(date_str, "%Y%m%d")
            except ValueError:
                pass
    return None

def get_file_creation_date(file_path):
    """Get the earliest date available: extracted or file system date."""
    extracted_date = extract_date_from_filename(os.path.basename(file_path))
    if extracted_date:
        return extracted_date
    return datetime.fromtimestamp(os.path.getmtime(file_path))

def cleanup_old_files(directory, days):
    """Remove files older than the specified number of days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    removed_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_creation_date = get_file_creation_date(file_path)
            
            if file_creation_date < cutoff_date:
                if not DRYRUN:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                removed_files.append(file_path)

    return removed_files

def remove_updates_data_json():
    """Remove the 'updates/data.json' file if it exists."""
    if os.path.exists(UPDATES_DATA_JSON):
        if not DRYRUN:
            os.remove(UPDATES_DATA_JSON)
            print(f"Removed: {UPDATES_DATA_JSON}")
        return UPDATES_DATA_JSON
    return None

def main():
    if DRYRUN:
        print("Dry Run mode enabled. No changes will be made.")
        return

    # Cleanup old files in the archive directory
    removed_files = cleanup_old_files(ARCHIVE_DIR, CLEANUP_PERIOD)

    # Remove updates/data.json
    removed_data_json = remove_updates_data_json()
    if removed_data_json:
        removed_files.append(removed_data_json)

    if removed_files:
        print("Files removed:", removed_files)
    else:
        print("No files to remove.")

if __name__ == "__main__":
    main()
