#!/usr/bin/env python3
"""
Transport Calculator launcher script.
Dit script start de Transport Calculator app direct vanuit de development omgeving.
"""

import os
import sys

# Voeg de huidige map toe aan het pad zodat we de src module kunnen importeren
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Start de applicatie
if __name__ == "__main__":
    print("Transport Calculator starten...")
    
    try:
        # Importeer en start de app
        from src.main import root
        root.mainloop()
    except Exception as e:
        print(f"Fout bij het starten van de app: {e}")
        import traceback
        traceback.print_exc()
        input("Druk op Enter om af te sluiten...") 