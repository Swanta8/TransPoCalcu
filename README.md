# Transport Calculator

Een desktop applicatie voor het berekenen van transportkosten inclusief personeel, brandstof, vaste kosten en toeslagen.

## Project Structuur

```
Transport Calculator/
  ├── src/                    # Broncode van de applicatie
  │   ├── __init__.py         # Python module markering
  │   ├── main.py             # Hoofdbestand met GUI
  │   ├── calculator.py       # Kostenberekeningen
  │   ├── vehicles.py         # Voertuigeninformatie
  │   └── config.py           # Configuratie-instellingen
  │
  ├── assets/                 # Resources (iconen, configuratie)
  │   ├── MetroUI.icns        # App icoon
  │   └── transport_config.json # Standaard configuratie
  │
  ├── build_tools/            # Scripts voor het bouwen van de applicatie
  │   ├── build_app.py        # Script voor bouwen van de app
  │   └── create_dmg.applescript # AppleScript voor DMG opmaak
  │
  ├── run.py                  # Script om de app te starten in ontwikkelomgeving
  └── README.md               # Project documentatie
```

## Snelstart

1. **App starten in ontwikkelomgeving**:
   ```
   python run.py
   ```
1.1 **App starten in terminal met alias in ~/.zshrc**
   '''
   transportcalc


2. **App bouwen voor distributie**:
   ```
   python build_tools/build_app.py
   ```

## App Functionaliteit

- Berekent transportkosten op basis van afstand, tijd en andere factoren
- Ondersteunt verschillende voertuigtypes
- Configureerbare prijzen en tarieven
- Verdiepingstoeslagen
- File-toeslagen

## Ontwikkeld voor

- macOS (Silicon en Intel)

## Ontwikkeld door

Transport Calculator is ontwikkeld voor intern gebruik. 