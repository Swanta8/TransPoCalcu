# calculator.py

from src.vehicles import vehicles
from src.config import config

def calculate_costs(
    distance_km,            # aantal km (enkele rit)
    travel_time_minutes,    # reistijd (min, enkele rit, excl. files)
    diesel_price,           # dieselprijs per liter
    staff_count,            # aantal personeel
    selected_vehicle,       # bv. "V980JS Mercedes Sprint"
    floor_number,           # verdieping (0 = begane grond, 3 = 3e etc.)
    location_time_hours     # tijd op locatie in uren
    
):
    """
    Berekent de totale kosten van een rit met:
    - Afstand (heen & terug)
    - File-toeslag op reistijd
    - Brandstofverbruik (km/l en prijs) of elektriciteitskosten (kWh/km)
    - Personeelskosten (reistijd + tijd op locatie)
    - Vaste kosten per rit
    - Verdiepingstoeslag vanaf 3e etage
    """

    # 1) Totale km = heen + terug
    total_km = distance_km * config["distance_factor"]

    # 2) File-toeslag op de totale reistijd
    traffic_factor = 1 + (config["traffic_surcharge_percentage"] / 100)
    total_travel_time_minutes = (travel_time_minutes * config["distance_factor"] / 2) * traffic_factor

    # 3) Tijd op locatie in minuten
    location_time_minutes = location_time_hours * 60

    # 4) Totaal aantal minuten dat personeel bezig is
    total_staff_minutes = total_travel_time_minutes + location_time_minutes

    # 5) Brandstof- of elektriciteitskosten
    info = vehicles[selected_vehicle]
    
    if info["is_electric"]:
        # Bereken elektriciteitskosten voor elektrische voertuigen
        kwh_used = total_km * info["kwh_per_km"]
        fuel_cost = kwh_used * info["electricity_cost_per_kwh"]
    else:
        # Brandstofkosten voor diesel/benzine voertuigen
        gem_km_per_l = info["gem_km_per_l"]
        liters_used = total_km / gem_km_per_l
        fuel_cost = liters_used * diesel_price

    # 6) Verdiepingstoeslag (vanaf geconfigureerde drempel)
    floor_surcharge = config["floor_surcharge"] if floor_number >= config["floor_threshold"] else 0

    # 7) Personeelskosten
    cost_per_minute = config["staff_hourly_rate"] / 60  # €/uur naar €/minuut
    staff_cost = total_staff_minutes * cost_per_minute * staff_count

    # 8) Vaste kosten per rit (berekend uit jaarlijkse lasten / aantal ritten * 2 voor retour)
    fixed_cost_per_ride = (config["annual_fixed_costs"] / config["annual_rides"]) * 2

    # 9) Totaal
    total_cost = fuel_cost + floor_surcharge + staff_cost + fixed_cost_per_ride

    return {
        "fuel_cost": fuel_cost,
        "floor_surcharge": floor_surcharge,
        "staff_cost": staff_cost,
        "fixed_cost_per_ride": fixed_cost_per_ride,
        "total_cost": total_cost
    }