#!/usr/bin/env python3
"""
Conversie script voor de Transport Calculator app.
Dit script zet het DMG bestand om naar een ZIP bestand met behulp van ditto.
"""

import os
import sys
import subprocess
import shutil
import tempfile
from datetime import datetime

# Project directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DMG_FILE = os.path.join(PROJECT_ROOT, "TransportCalculator.dmg")
ZIP_FILE = os.path.join(PROJECT_ROOT, "TransportCalculator.zip")
APP_NAME = "Transport Calculator.app"

def run_command(cmd, timeout=60):
    """Execute a command with timeout"""
    print(f"Uitvoeren: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            print(f"Waarschuwing: commando returncode {result.returncode}")
            if result.stderr:
                print(f"Fout: {result.stderr}")
        return result
    except subprocess.TimeoutExpired:
        print(f"Timeout na {timeout} seconden voor commando: {' '.join(cmd)}")
        return None

def convert_using_temp_directory():
    """
    Converteer DMG naar ZIP via een tijdelijke directory en ditto.
    Deze methode gebruikt 'ditto' om een ECHTE ZIP te maken (geen omgenoemde DMG).
    """
    print("DMG naar ZIP conversie via temp directory...")
    
    # Maak temp directories
    temp_mount_dir = tempfile.mkdtemp(prefix="dmg_mount_")
    temp_extract_dir = tempfile.mkdtemp(prefix="dmg_extract_")
    success = False
    
    try:
        # First, try to detach any existing mounts of our DMG
        print("Opschonen van bestaande mounts...")
        info_cmd = ["hdiutil", "info"]
        info_result = run_command(info_cmd)
        
        if info_result and info_result.returncode == 0:
            for line in info_result.stdout.splitlines():
                if DMG_FILE in line:
                    # Zoek naar volumes die aan deze DMG zijn gekoppeld
                    for vol_line in info_result.stdout.splitlines():
                        if "/Volumes/" in vol_line and "disk" in vol_line:
                            vol_path = vol_line.split()[-1]
                            print(f"Unmounting volume: {vol_path}")
                            detach_cmd = ["hdiutil", "detach", vol_path, "-force"]
                            run_command(detach_cmd)
        
        # Mount DMG bestand
        print("DMG bestand mounten...")
        mount_cmd = ["hdiutil", "attach", DMG_FILE, "-mountpoint", temp_mount_dir, "-nobrowse", "-noverify"]
        result = run_command(mount_cmd, timeout=30)
        
        if not result or result.returncode != 0:
            print("Fout bij het mounten van het DMG bestand! Probeer alternatieve methode...")
            return try_ditto_direct_conversion()
        
        print(f"DMG gemount op: {temp_mount_dir}")
        print(f"Bestanden in gemounte DMG: {os.listdir(temp_mount_dir)}")
        
        # Kopieer relevante bestanden naar tijdelijke directory
        print("Bestanden kopiëren naar tijdelijke directory...")
        app_found = False
        
        for item in os.listdir(temp_mount_dir):
            src_path = os.path.join(temp_mount_dir, item)
            dst_path = os.path.join(temp_extract_dir, item)
            
            # Sla hidden files en DS_Store bestanden over
            if item.startswith('.') and item != '.VolumeIcon.icns':
                continue
                
            if os.path.isdir(src_path):
                print(f"Map kopiëren: {item}")
                shutil.copytree(src_path, dst_path)
                if item.endswith('.app'):
                    app_found = True
            else:
                print(f"Bestand kopiëren: {item}")
                shutil.copy2(src_path, dst_path)
        
        if not app_found:
            print("Waarschuwing: Geen .app bestand gevonden in de DMG.")
        
        # Unmount DMG
        print("DMG unmounten...")
        unmount_cmd = ["hdiutil", "detach", temp_mount_dir, "-force"]
        run_command(unmount_cmd, timeout=20)
        
        # Verwijder oude ZIP indien aanwezig
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
        
        # Gebruik ditto om ZIP bestand te maken (ditto maakt standaard compatibele ZIPs)
        print("ZIP bestand maken met ditto...")
        ditto_cmd = ["ditto", "-c", "-k", "--keepParent", "--rsrc", temp_extract_dir, ZIP_FILE]
        result = run_command(ditto_cmd, timeout=120)
        
        if not result or result.returncode != 0:
            print("Fout bij het maken van ZIP bestand met ditto!")
            return False
        
        # Verify ZIP file exists and has content
        if os.path.exists(ZIP_FILE) and os.path.getsize(ZIP_FILE) > 0:
            zip_size = os.path.getsize(ZIP_FILE) / (1024 * 1024)  # Size in MB
            print(f"ZIP bestand succesvol gemaakt: {ZIP_FILE}")
            print(f"ZIP bestandsgrootte: {zip_size:.2f} MB")
            success = True
        else:
            print(f"Fout: ZIP bestand werd niet correct aangemaakt")
            success = False
            
    except Exception as e:
        print(f"Fout tijdens conversie: {e}")
        success = False
    
    finally:
        # Cleanup
        print("Opruimen...")
        
        # Make sure DMG is unmounted
        if os.path.exists(temp_mount_dir) and os.path.ismount(temp_mount_dir):
            unmount_cmd = ["hdiutil", "detach", temp_mount_dir, "-force"]
            run_command(unmount_cmd)
        
        # Remove temp directories
        for d in [temp_mount_dir, temp_extract_dir]:
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                    print(f"Directory verwijderd: {d}")
                except Exception as e:
                    print(f"Waarschuwing: Kan directory niet verwijderen {d}: {e}")
    
    return success

def try_ditto_direct_conversion():
    """
    Probeer direct conversie naar ZIP met ditto vanuit dist directory.
    Deze methode gebruikt de gecompileerde app in de dist directory.
    """
    print("Alternatieve methode: gebruik ditto direct met app uit dist directory...")
    
    # Check if the app exists in the dist directory
    dist_dir = os.path.join(PROJECT_ROOT, "dist")
    app_path = os.path.join(dist_dir, APP_NAME)
    
    if not os.path.exists(app_path):
        print(f"Fout: App niet gevonden in {dist_dir}")
        return False
    
    try:
        # Verwijder oude ZIP indien aanwezig
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
        
        # Gebruik ditto om ZIP bestand te maken van de app
        print(f"ZIP bestand maken van app: {app_path}")
        ditto_cmd = ["ditto", "-c", "-k", "--keepParent", "--rsrc", app_path, ZIP_FILE]
        result = run_command(ditto_cmd, timeout=120)
        
        if not result or result.returncode != 0:
            print("Fout bij het maken van ZIP bestand met ditto!")
            return False
        
        # Verify ZIP file exists and has content
        if os.path.exists(ZIP_FILE) and os.path.getsize(ZIP_FILE) > 0:
            zip_size = os.path.getsize(ZIP_FILE) / (1024 * 1024)  # Size in MB
            print(f"ZIP bestand succesvol gemaakt: {ZIP_FILE}")
            print(f"ZIP bestandsgrootte: {zip_size:.2f} MB")
            return True
        else:
            print(f"Fout: ZIP bestand werd niet correct aangemaakt")
            return False
            
    except Exception as e:
        print(f"Fout tijdens directe conversie: {e}")
        return False

def main():
    """Hoofdfunctie voor het conversieproces"""
    start_time = datetime.now()
    print(f"DMG naar ZIP conversie starten... ({start_time.strftime('%H:%M:%S')})")
    
    # Controleer of DMG bestand bestaat
    if not os.path.exists(DMG_FILE):
        print(f"Fout: DMG bestand '{DMG_FILE}' niet gevonden!")
        
        # Als DMG niet bestaat, probeer direct vanuit de app directory
        if try_ditto_direct_conversion():
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"Directe app conversie voltooid in {elapsed:.2f} seconden!")
            sys.exit(0)
        else:
            print("Conversie gefaald!")
            sys.exit(1)
    
    dmg_size = os.path.getsize(DMG_FILE) / (1024 * 1024)  # Size in MB
    print(f"DMG bestandsgrootte: {dmg_size:.2f} MB")
    
    # Converteer DMG naar standaard ZIP formaat
    if convert_using_temp_directory():
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"Conversie voltooid in {elapsed:.2f} seconden!")
        sys.exit(0)
    else:
        print("Primaire conversie methode gefaald!")
        
        # Probeer de directe conversie als fallback
        if try_ditto_direct_conversion():
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"Fallback conversie voltooid in {elapsed:.2f} seconden!")
            sys.exit(0)
        else:
            print("Alle conversiemethoden gefaald!")
            sys.exit(1)

if __name__ == "__main__":
    main() 