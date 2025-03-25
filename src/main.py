# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from src.calculator import calculate_costs
from src.vehicles import vehicles
from src.config import config, save_config, reset_to_default, validate_numeric

# Configuratiescherm
def open_config_window():
    config_window = tk.Toplevel(root)
    config_window.title("Configuratie Instellingen")
    config_window.grab_set()  # Maak het venster modaal
    
    # Maak entry widgets voor elke configuratieparameter
    entries = {}
    row = 0
    
    # Helper functie voor validatie bij verlaten van veld
    def validate_entry(entry, key, min_val=0, max_val=None, is_int=False):
        def validate():
            value = entry.get()
            if not validate_numeric(value, min_val, max_val, is_int):
                messagebox.showerror("Invoerfout", f"Ongeldige waarde voor {key}. Waarde moet een getal zijn" +
                                    (f" tussen {min_val} en {max_val}" if max_val else f" groter dan {min_val}") +
                                    (", en geheel getal" if is_int else ""))
                entry.focus_set()
                return False
            return True
        return validate
    
    # Personeelskosten per uur
    tk.Label(config_window, text="Personeelskosten per uur (€):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
    staff_rate_entry = tk.Entry(config_window)
    staff_rate_entry.insert(0, str(config["staff_hourly_rate"]))
    staff_rate_entry.grid(row=row, column=1, padx=5, pady=5)
    entries["staff_hourly_rate"] = (staff_rate_entry, validate_entry(staff_rate_entry, "Personeelskosten", 1))
    row += 1
    
    # Jaarlijkse vaste lasten
    tk.Label(config_window, text="Jaarlijkse vaste lasten (€):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
    annual_costs_entry = tk.Entry(config_window)
    annual_costs_entry.insert(0, str(config["annual_fixed_costs"]))
    annual_costs_entry.grid(row=row, column=1, padx=5, pady=5)
    entries["annual_fixed_costs"] = (annual_costs_entry, validate_entry(annual_costs_entry, "Jaarlijkse vaste lasten", 0))
    row += 1
    
    # Aantal ritten per jaar
    tk.Label(config_window, text="Aantal ritten per jaar:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
    annual_rides_entry = tk.Entry(config_window)
    annual_rides_entry.insert(0, str(config["annual_rides"]))
    annual_rides_entry.grid(row=row, column=1, padx=5, pady=5)
    entries["annual_rides"] = (annual_rides_entry, validate_entry(annual_rides_entry, "Aantal ritten", 1, is_int=True))
    row += 1
    
    # Verdiepingstoeslag bedrag
    tk.Label(config_window, text="Verdiepingstoeslag bedrag (€):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
    floor_surcharge_entry = tk.Entry(config_window)
    floor_surcharge_entry.insert(0, str(config["floor_surcharge"]))
    floor_surcharge_entry.grid(row=row, column=1, padx=5, pady=5)
    entries["floor_surcharge"] = (floor_surcharge_entry, validate_entry(floor_surcharge_entry, "Verdiepingstoeslag", 0))
    row += 1
    
    # Verdiepingsdrempel
    tk.Label(config_window, text="Verdiepingsdrempel (vanaf etage):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
    floor_threshold_entry = tk.Entry(config_window)
    floor_threshold_entry.insert(0, str(config["floor_threshold"]))
    floor_threshold_entry.grid(row=row, column=1, padx=5, pady=5)
    entries["floor_threshold"] = (floor_threshold_entry, validate_entry(floor_threshold_entry, "Verdiepingsdrempel", 0, 7, is_int=True))
    row += 1
    
    # File-toeslag percentage
    tk.Label(config_window, text="File-toeslag percentage (%):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
    traffic_entry = tk.Entry(config_window)
    traffic_entry.insert(0, str(config["traffic_surcharge_percentage"]))
    traffic_entry.grid(row=row, column=1, padx=5, pady=5)
    entries["traffic_surcharge_percentage"] = (traffic_entry, validate_entry(traffic_entry, "File-toeslag", 0, 100))
    row += 1
    
    # Totale km factor
    tk.Label(config_window, text="Totale km factor (enkele rit x):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
    distance_factor_entry = tk.Entry(config_window)
    distance_factor_entry.insert(0, str(config["distance_factor"]))
    distance_factor_entry.grid(row=row, column=1, padx=5, pady=5)
    entries["distance_factor"] = (distance_factor_entry, validate_entry(distance_factor_entry, "Km factor", 1))
    row += 1
    
    # Functie om configuratie op te slaan
    def save_settings():
        # Valideer alle velden
        for key, (entry, validator) in entries.items():
            if not validator():
                return
            
            # Zet waarde om naar juiste type en sla op in config
            value = entry.get()
            if key in ["annual_rides", "floor_threshold"]:
                config[key] = int(value)
            else:
                config[key] = float(value)
        
        # Sla op en sluit het venster
        if save_config():
            messagebox.showinfo("Configuratie", "Instellingen succesvol opgeslagen")
            config_window.destroy()
        else:
            messagebox.showerror("Fout", "Kon instellingen niet opslaan")
    
    # Functie om terug te gaan naar standaardwaarden
    def reset_settings():
        if messagebox.askyesno("Reset", "Weet u zeker dat u alle instellingen wilt resetten naar standaardwaarden?"):
            reset_config = reset_to_default()
            
            # Update alle velden met standaardwaarden
            for key, (entry, _) in entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, str(reset_config[key]))
            
            messagebox.showinfo("Reset", "Instellingen zijn gereset naar standaardwaarden")
    
    # Knoppen
    btn_frame = tk.Frame(config_window)
    btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
    
    tk.Button(btn_frame, text="Opslaan", command=save_settings).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Reset naar standaard", command=reset_settings).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Annuleren", command=config_window.destroy).pack(side=tk.LEFT, padx=5)

def on_calculate():
    try:
        # Lees de invoervelden uit
        distance_km = float(entry_distance.get())
        travel_time_minutes = float(entry_time.get())
        diesel_price = float(entry_price.get())
        staff_count = int(entry_staff.get())
        location_time_hours = float(entry_location_hours.get())

        selected_vehicle = cmb_vehicle.get()    # tekst, bv. "V980JS Mercedes Sprint"
        selected_floor_text = cmb_floor.get()   # bv. "3e etage"

        # Verdieping omzetten naar integer
        if selected_floor_text == "Begane grond":
            floor_number = 0
        else:
            floor_number = int(selected_floor_text.split("e")[0])

        # Berekening uitvoeren
        result = calculate_costs(
            distance_km=distance_km,
            travel_time_minutes=travel_time_minutes,
            diesel_price=diesel_price,
            staff_count=staff_count,
            selected_vehicle=selected_vehicle,
            floor_number=floor_number,
            location_time_hours=location_time_hours
        )

        # Resultaat tonen
        output_text = (
            f"Brandstof: €{result['fuel_cost']:.2f}\n"
            f"Personeel: €{result['staff_cost']:.2f}\n"
            f"Vaste kosten: €{result['fixed_cost_per_ride']:.2f}\n"
            f"Verdieping: €{result['floor_surcharge']:.2f}\n"
            f"----------------------------\n"
            f"Totaal: €{result['total_cost']:.2f}"
        )
        lbl_result.config(text=output_text)

    except ValueError:
        lbl_result.config(text="Fout bij invoer: controleer of alles numeriek is.")

# --- GUI opbouw ---
root = tk.Tk()
root.title("Transport Calculator")

# Maak menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Bestand menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Bestand", menu=file_menu)
file_menu.add_command(label="Configuratie", command=open_config_window)
file_menu.add_separator()
file_menu.add_command(label="Afsluiten", command=root.quit)

# 1) Aantal KM (enkele rit)
tk.Label(root, text="Aantal KM (enkele rit):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_distance = tk.Entry(root)
entry_distance.insert(0, "14")  # voorbeeld
entry_distance.grid(row=0, column=1, padx=5, pady=5)

# 2) Reistijd (min, enkele rit)
tk.Label(root, text="Reistijd (min, enkele rit):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_time = tk.Entry(root)
entry_time.insert(0, "19")
entry_time.grid(row=1, column=1, padx=5, pady=5)

# 3) Dieselprijs
tk.Label(root, text="Dieselprijs (€/L):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_price = tk.Entry(root)
entry_price.insert(0, "1.84")
entry_price.grid(row=2, column=1, padx=5, pady=5)

# 4) Aantal personeel
tk.Label(root, text="Aantal personeel:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_staff = tk.Entry(root)
entry_staff.insert(0, "2")
entry_staff.grid(row=3, column=1, padx=5, pady=5)

# 5) Tijd op locatie (in uren)
tk.Label(root, text="Tijd op locatie (uren):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
entry_location_hours = tk.Entry(root)
entry_location_hours.insert(0, "1.0")  # voorbeeld
entry_location_hours.grid(row=4, column=1, padx=5, pady=5)

# 6) Keuze Voertuig (dropdown)
tk.Label(root, text="Voertuig:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
cmb_vehicle = ttk.Combobox(root, values=list(vehicles.keys()), width=30)
cmb_vehicle.current(0)
cmb_vehicle.grid(row=5, column=1, padx=5, pady=5)

# 7) Keuze Verdieping (dropdown)
tk.Label(root, text="Verdieping:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
floors = ["Begane grond", "1e etage", "2e etage", "3e etage", "4e etage", "5e etage", "6e etage", "7e etage"]
cmb_floor = ttk.Combobox(root, values=floors, width=30)
cmb_floor.current(0)
cmb_floor.grid(row=6, column=1, padx=5, pady=5)

# Configuratieknop
btn_config = tk.Button(root, text="Configuratie", command=open_config_window)
btn_config.grid(row=7, column=0, padx=5, pady=5, sticky="w")

# 8) Knop Bereken
btn_calc = tk.Button(root, text="Bereken", command=on_calculate)
btn_calc.grid(row=7, column=1, pady=10, sticky="e")

# 9) Label voor resultaat
lbl_result = tk.Label(root, text="Resultaat verschijnt hier...")
lbl_result.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()