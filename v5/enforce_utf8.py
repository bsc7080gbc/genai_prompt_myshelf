import chardet
import sys
import os

def is_utf8(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding'] == 'utf-8'

def validate_files(file_list):
    all_valid = True
    for file_path in file_list:
        if not os.path.isfile(file_path):
            print(f"Skipping non-existent file: {file_path}")
            continue
        if not is_utf8(file_path):
            print(f"Non-UTF-8 file detected: {file_path}")
            all_valid = False
    if not all_valid:
        sys.exit(1)  # Exit with error code if any file is non-UTF-8
    else:
        print("All files are UTF-8 compliant.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enforce_utf8.py --filelist <filelist>")
        sys.exit(1)

    filelist_path = sys.argv[2]
    if not os.path.isfile(filelist_path):
        print(f"File list {filelist_path} does not exist.")
        sys.exit(1)

    with open(filelist_path, 'r') as f:
        files = [line.strip() for line in f.readlines() if line.strip()]

    if not files:
        print("No files to validate. Skipping UTF-8 enforcement.")
        sys.exit(0)

    validate_files(files)
