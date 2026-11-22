"""Append flights for new routes (both directions) to data/flights.json."""
import json
import random

ROUTES = [("Bangalore", "Chennai"), ("Mumbai", "Goa")]  # add your pairs here
AIRLINES = ["IndiGo", "Air India", "SpiceJet", "Vistara"]
PATH = "data/flights.json"

with open(PATH, encoding="utf-8") as f:
    flights = json.load(f)

next_id = len(flights) + 1
for a, b in ROUTES:
    for source, destination in ((a, b), (b, a)):
        for _ in range(3):  # three flights per direction
            hour = random.randint(5, 20)
            duration = random.randint(1, 3)
            flights.append({
                "flight_id": f"FL{next_id:04d}",
                "airline": random.choice(AIRLINES),
                "from": source,
                "to": destination,
                "departure_time": f"2026-11-25T{hour:02d}:00:00",
                "arrival_time": f"2026-11-25T{hour + duration:02d}:00:00",
                "price": random.randint(2500, 7000),
            })
            next_id += 1

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(flights, f, indent=2)
print(f"Now {len(flights)} flights.")