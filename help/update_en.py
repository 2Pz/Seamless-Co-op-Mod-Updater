import json
import os
import sys

# Set the default encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

# Path to the JSON file
json_file_path = "localization/en.json"

# New key and value to be added
new_key = "ui.settings.backup.max_backups"
new_value = "Max Backups:"

# Function to update the dictionary with nested keys
def add_nested_key(data, keys, value):
    key = keys[0]
    if len(keys) > 1:
        if key not in data:
            data[key] = {}
        add_nested_key(data[key], keys[1:], value)
    else:
        data[key] = value

# Load the JSON data
if os.path.exists(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

# Split the key string into a nested structure
key_parts = new_key.split(".")

# Update the JSON data with the new key-value pair
add_nested_key(data, key_parts, new_value)

# Save the updated JSON back to the file
with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_key}: '{new_value}' to the JSON file.")


