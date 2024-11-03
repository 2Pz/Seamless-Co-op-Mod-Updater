import sys
from cx_Freeze import setup, Executable
import os
from version import VERSION
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Include necessary files without including source code
include_files = [
    ('assets/', 'assets/'),
    ('localization/', 'localization/'),
    ('.env', '.env'),  # Include the .env file
]

# Add additional options like packages and excludes
build_exe_options = {
    'packages': ['os', 'sys', 'pefile', 'PyQt6', 'dotenv'],  # Add dotenv to the packages
    'excludes': ['tkinter'],  # Exclude any unused packages
    'include_files': include_files,
    'zip_include_packages': ['*'],  # Compress packages into a zip file
    'zip_exclude_packages': [],     # Exclude no packages from the zip file
    'build_exe': 'build/seamlesscoop_Manager',  # Customize build output path
    'optimize': 2  # Optimize .pyc files (2 strips docstrings)
}

# Base for the executable
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'  # For a Windows GUI app

# Define the main executable and other necessary options
executables = [
    Executable(
        'main.py',  # The main script of your project
        base=base,
        target_name=f'SeamlessCo-opManager_{VERSION}.exe',  # Output executable name
        icon='assets/update.ico'  # Path to the icon file
    )
]

# Setup configuration
setup(
    name=f'SeamlessCo-opManager_{VERSION}',
    version=VERSION,
    description='A Seamless Co-op Manager for Elden Ring',
    options={'build_exe': build_exe_options},
    executables=executables
)

# python setup.py build