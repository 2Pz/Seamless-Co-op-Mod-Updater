import json
import os

# Path to the JSON file
json_file_path = "localization/en.json"

# Function to search for a nested key in the dictionary
def search_nested_key(data, keys):
    key = keys[0]
    if len(keys) > 1:
        if key in data:
            return search_nested_key(data[key], keys[1:])
        else:
            return None
    else:
        return data.get(key)

# Load the JSON data
if os.path.exists(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    print("JSON file does not exist.")
    data = {}

# Key to search for
search_key = "ui.settings.backup.key_binds"  # Change this to the key you want to search for

# Split the key string into a nested structure
key_parts = search_key.split(".")

# Search for the key in the JSON data
result = search_nested_key(data, key_parts)

if result is not None:
    print(f"Found {search_key}: '{result}'")
else:
    print(f"{search_key} not found in the JSON file.")