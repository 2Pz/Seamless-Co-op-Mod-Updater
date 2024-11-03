import json
import os

def load_json(file_path):
    """Load a JSON file and return its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(file_path, content):
    """Save the modified content back to the JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)

def compare_and_update(en_json, target_json):
    """Recursively compare two dictionaries to add missing keys and remove extra keys."""
    # Remove extra keys in the target JSON that are not present in the English JSON
    extra_keys = [key for key in target_json if key not in en_json]
    for key in extra_keys:
        del target_json[key]

    # Add missing keys or recursively update dictionaries
    for key, value in en_json.items():
        if key not in target_json:
            # If key is missing, add it with the English text
            target_json[key] = value
        elif isinstance(value, dict):
            # If both values are dictionaries, recursively check for missing keys
            compare_and_update(value, target_json[key])

def update_language_files(en_file, other_files_dir):
    """Compare the English JSON with other language files and update them."""
    # Load the English JSON file
    en_content = load_json(en_file)
    
    # Loop through the other language files in the directory
    for file_name in os.listdir(other_files_dir):
        if file_name.endswith('.json') and file_name != os.path.basename(en_file):
            # Load the target language JSON file
            file_path = os.path.join(other_files_dir, file_name)
            target_content = load_json(file_path)
            
            # Compare and update the target JSON file with missing keys and remove extra keys
            compare_and_update(en_content, target_content)
            
            # Save the updated content back to the file
            save_json(file_path, target_content)
            print(f'Updated: {file_name}')

if __name__ == '__main__':
    # Path to the en.json file
    en_file_path = r'localization/en.json'
    
    # Directory containing other language JSON files (e.g., ar.json, fr.json)
    other_files_directory = 'localization'
    
    # Update all language files with missing keys from en.json
    update_language_files(en_file_path, other_files_directory)
