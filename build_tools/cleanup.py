#!/usr/bin/env python3
"""
Cleanup Script voor Transport Calculator project.
Verwijdert tijdelijke en dubbele bestanden uit het project.
"""

import os
import shutil
import sys

# Project directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Bestanden die altijd mogen worden verwijderd
TEMP_FILES = [
    '*.pyc',
    '*.pyo',
    '*.spec',
    'calculator.py',  # oude bestand in hoofdmap
    'main.py',        # oude bestand in hoofdmap
    'vehicles.py',    # oude bestand in hoofdmap
    'config.py',      # oude bestand in hoofdmap
    'transport_config.json',  # oude bestand in hoofdmap
    'create_dmg.applescript',  # oude bestand in hoofdmap
]

# Mappen die mogen worden verwijderd
TEMP_DIRS = [
    '__pycache__',
    'dmg_temp',
]

def cleanup_files():
    """Verwijder tijdelijke bestanden uit het project"""
    print("Tijdelijke bestanden opschonen...")
    
    # Verwijder individuele bestanden
    for pattern in TEMP_FILES:
        if '*' in pattern:
            # Wildcard pattern, vind alle bestanden
            import glob
            for file_path in glob.glob(os.path.join(PROJECT_ROOT, pattern)):
                try:
                    os.remove(file_path)
                    print(f"  Verwijderd: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"  Fout bij verwijderen {file_path}: {e}")
        else:
            # Exact bestandspad
            file_path = os.path.join(PROJECT_ROOT, pattern)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"  Verwijderd: {pattern}")
                except Exception as e:
                    print(f"  Fout bij verwijderen {pattern}: {e}")

def cleanup_dirs():
    """Verwijder tijdelijke mappen uit het project"""
    print("Tijdelijke mappen opschonen...")
    
    for dir_name in TEMP_DIRS:
        # Zoek in de hoofdmap
        dir_path = os.path.join(PROJECT_ROOT, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"  Verwijderd: {dir_name}/")
            except Exception as e:
                print(f"  Fout bij verwijderen {dir_name}/: {e}")
        
        # Zoek ook recursief in alle submappen
        for root, dirs, files in os.walk(PROJECT_ROOT):
            if dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"  Verwijderd: {os.path.relpath(dir_path, PROJECT_ROOT)}")
                except Exception as e:
                    print(f"  Fout bij verwijderen {os.path.relpath(dir_path, PROJECT_ROOT)}: {e}")

def main():
    """Hoofdfunctie voor het opschoonproces"""
    print("Transport Calculator project opschonen...")
    
    cleanup_files()
    cleanup_dirs()
    
    print("Project opgeschoond!")

if __name__ == "__main__":
    main() 