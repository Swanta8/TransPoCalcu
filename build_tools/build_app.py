#!/usr/bin/env python3
"""
Build script voor de Transport Calculator app.
Dit script bouwt de app en creëert een DMG bestand.
"""

import os
import sys
import subprocess
import shutil

# Project directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets')
BUILD_DIR = os.path.join(PROJECT_ROOT, 'build')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')
DMG_TEMP_DIR = os.path.join(PROJECT_ROOT, 'dmg_temp')

# App configuration
APP_NAME = "Transport Calculator"
ICON_FILE = os.path.join(ASSETS_DIR, "MetroUI.icns")
CONFIG_FILE = os.path.join(ASSETS_DIR, "transport_config.json")
MAIN_SCRIPT = os.path.join(SRC_DIR, "main.py")

def clean_build_dirs():
    """Maak bouwdirectories schoon"""
    print("Schoonmaken van build directories...")
    
    # Verwijder bestaande directories indien aanwezig
    for dir_path in [DMG_TEMP_DIR]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    
    # Maak dmg_temp directory aan
    os.makedirs(DMG_TEMP_DIR, exist_ok=True)

def build_app():
    """Bouw de app met PyInstaller"""
    print(f"Bouwen van {APP_NAME} app...")
    
    # PyInstaller commando samenstellen
    cmd = [
        "pyinstaller",
        "--windowed",
        f"--name={APP_NAME}",
        f"--icon={ICON_FILE}",
        f"--add-data={CONFIG_FILE}:.",
        "--clean",
        "-y",
        MAIN_SCRIPT
    ]
    
    # Voer PyInstaller uit
    process = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if process.returncode != 0:
        print("Fout bij het bouwen van de app!")
        sys.exit(1)
    
    print("App succesvol gebouwd!")

def create_dmg():
    """Maak een DMG bestand met create-dmg"""
    print("DMG bestand maken...")
    
    # Kopieer app naar dmg_temp directory
    app_path = os.path.join(DIST_DIR, f"{APP_NAME}.app")
    shutil.copytree(app_path, os.path.join(DMG_TEMP_DIR, f"{APP_NAME}.app"))
    
    # Verwijder oude DMG indien aanwezig
    dmg_file = os.path.join(PROJECT_ROOT, "TransportCalculator.dmg")
    if os.path.exists(dmg_file):
        os.remove(dmg_file)
    
    # create-dmg commando samenstellen
    cmd = [
        "create-dmg",
        f"--volname={APP_NAME}",
        f"--volicon={ICON_FILE}",
        "--window-pos=200",
        "120",
        "--window-size=500",
        "320",
        "--icon-size=100",
        f"--icon={APP_NAME}.app",
        "125",
        "150",
        "--app-drop-link",
        "375",
        "150",
        "--no-internet-enable",
        "TransportCalculator.dmg",
        "dmg_temp/"
    ]
    
    # Voer create-dmg uit
    process = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if process.returncode != 0:
        print("Fout bij het maken van het DMG bestand!")
        sys.exit(1)
    
    print("DMG bestand succesvol gemaakt!")

def cleanup():
    """Schoonmaken na het bouwen"""
    print("Opruimen...")
    
    # Verwijder tijdelijke dmg directory
    if os.path.exists(DMG_TEMP_DIR):
        shutil.rmtree(DMG_TEMP_DIR)
    
    print("Klaar!")

def main():
    """Hoofdfunctie voor het bouwproces"""
    print(f"Bouwen van {APP_NAME}...")
    
    clean_build_dirs()
    build_app()
    create_dmg()
    cleanup()
    
    print(f"{APP_NAME} is succesvol gebouwd!")
    print(f"De app is beschikbaar in: {os.path.join(DIST_DIR, APP_NAME + '.app')}")
    print(f"Het DMG bestand is beschikbaar in: {os.path.join(PROJECT_ROOT, 'TransportCalculator.dmg')}")

if __name__ == "__main__":
    main() 