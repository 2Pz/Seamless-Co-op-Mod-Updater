import os

def print_structure(root_dir, indent=0):
    # Print the current folder, excluding the .venv folder
    folder_name = os.path.basename(root_dir)
    if folder_name != '.venv':
        print('    ' * indent + folder_name + '/')

        # Print the files in the current directory
        for file in os.listdir(root_dir):
            file_path = os.path.join(root_dir, file)
            if os.path.isfile(file_path):
                if file.endswith('.py'):
                    print('    ' * (indent + 1) + f'- {file}')
                elif file.endswith('.png') or file.endswith('.ico'):
                    print('    ' * (indent + 1) + f'- {file}')

        # Print subdirectories and their contents
        for dir in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir)
            if os.path.isdir(dir_path):
                print_structure(dir_path, indent + 1)

if __name__ == "__main__":
    # Set the root directory to the specified path
    root_directory = r"D:\Users\Ali\Documents\Vscode_project\SeamlessCo-opUpdater-v2"
    print_structure(root_directory)
