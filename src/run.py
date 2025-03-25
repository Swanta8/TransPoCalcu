#!/usr/bin/env python3
"""
Transport Calculator launcher script.
Dit script start de Transport Calculator app direct vanuit de development omgeving.
"""

import os
import sys
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG to show all messages
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Voeg de huidige map toe aan het pad zodat we de src module kunnen importeren
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import logging utils first
from src.log_utils import setup_file_logging, log_app, log_error, LogCategory, log_message

# Start de applicatie
if __name__ == "__main__":
    log_app("Transport Calculator wordt gestart...")
    log_app(f"Python versie: {sys.version}")
    log_app(f"Werkdirectory: {os.getcwd()}")
    
    # Setup file logging
    setup_file_logging()
    
    start_time = time.time()
    
    try:
        log_app("Modules laden...")
        # Importeer en start de app
        from src.main import root, on_calculate
        
        log_app("Configuratie geladen")
        log_app("UI geïnitialiseerd")
        log_app(f"Transport Calculator app gestart in {time.time() - start_time:.2f} seconden")
        
        # Monkey patch de on_calculate functie om logging toe te voegen
        original_on_calculate = on_calculate
        
        def on_calculate_with_logging():
            log_app("Berekening gestart...")
            start_calc = time.time()
            original_on_calculate()
            log_app(f"Berekening voltooid in {time.time() - start_calc:.4f} seconden")
        
        # Replace the original function with our logging version
        import src.main
        src.main.on_calculate = on_calculate_with_logging
        
        # Start de main loop
        log_app("App UI wordt gestart. Wacht op gebruikersinteractie...")
        root.mainloop()
        log_app("App afgesloten")
        
    except Exception as e:
        log_error(f"Fout bij het starten van de app: {e}")
        import traceback
        log_message(logging.ERROR, LogCategory.ERROR, traceback.format_exc())
        input("Druk op Enter om af te sluiten...") 