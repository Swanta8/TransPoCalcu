import json
import os
import sys

# Standaard configuratiewaarden
DEFAULT_CONFIG = {
    "staff_hourly_rate": 30.0,            # Personeelskosten per uur (€)
    "annual_fixed_costs": 77167.8,        # Jaarlijkse vaste lasten (€)
    "annual_rides": 862,                  # Aantal ritten per jaar
    "floor_surcharge": 200.0,             # Verdiepingstoeslag bedrag (€)
    "floor_threshold": 3,                 # Verdiepingsdrempel (vanaf welke etage toeslag)
    "traffic_surcharge_percentage": 15.0, # File-toeslag percentage
    "distance_factor": 4.0                # Totale km factor (hoeveel keer enkele rit)
}

# Bepaal het configuratiebestandspad: gebruik gebruikersmap voor de standalone app
def get_config_path():
    # In een PyInstaller bundel, gebruik gebruikersmap voor de configuratie
    if getattr(sys, 'frozen', False):
        config_dir = os.path.join(os.path.expanduser("~"), ".transportcalculator")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, "transport_config.json")
    else:
        # In ontwikkelomgeving, gebruik huidige map
        return "transport_config.json"

CONFIG_FILE = get_config_path()

# Globale configuratie variabele
config = {}

def load_config():
    """Laad configuratie uit bestand of gebruik standaardwaarden"""
    global config
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                
            # Controleer of alle vereiste sleutels aanwezig zijn, voeg toe indien nodig
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
        except Exception as e:
            print(f"Fout bij laden configuratie: {e}")
            config = DEFAULT_CONFIG.copy()
    else:
        config = DEFAULT_CONFIG.copy()
        save_config()  # Maak het configuratiebestand aan
    
    return config

def save_config():
    """Sla de huidige configuratie op"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Fout bij opslaan configuratie: {e}")
        return False

def reset_to_default():
    """Reset de configuratie naar standaardwaarden"""
    global config
    config = DEFAULT_CONFIG.copy()
    save_config()
    return config

def validate_numeric(value, min_value=None, max_value=None, is_int=False):
    """Valideer een numerieke waarde binnen bereik"""
    try:
        if is_int:
            val = int(value)
        else:
            val = float(value)
            
        if min_value is not None and val < min_value:
            return False
        if max_value is not None and val > max_value:
            return False
        return True
    except ValueError:
        return False

# Laad configuratie bij importeren van module
load_config() 