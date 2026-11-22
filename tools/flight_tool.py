"""Flight search tool."""
from datetime import datetime
from utils import load_json, same_text


def _duration_minutes(flight: dict) -> int:
    dep = datetime.fromisoformat(flight["departure_time"])
    arr = datetime.fromisoformat(flight["arrival_time"])
    return int((arr - dep).total_seconds() // 60)


def search_flights(source: str, destination: str, date: str = None,
                   sort_by: str = "cheapest", limit: int = 3) -> dict:
    """Find flights from source to destination.

    Args:
        source: departure city.
        destination: arrival city.
        date: optional 'YYYY-MM-DD'. If no flight matches, any date is used.
        sort_by: 'cheapest' or 'fastest'.
        limit: how many options to return.
    """
    flights = [f for f in load_json("flights.json")
               if same_text(f["from"], source) and same_text(f["to"], destination)]
    if not flights:
        return {"found": False, "message": f"No flights from {source} to {destination}.",
                "options": []}

    note = ""
    if date:
        on_date = [f for f in flights if f["departure_time"].startswith(date)]
        if on_date:
            flights = on_date
        else:
            note = (f"No flight on {date}; these are the available flights on this "
                    f"route (dataset dates are indicative).")

    for f in flights:
        f["duration_minutes"] = _duration_minutes(f)

    key = "duration_minutes" if sort_by == "fastest" else "price"
    flights.sort(key=lambda f: f[key])
    return {"found": True, "note": note, "sorted_by": sort_by, "options": flights[:limit]}


if __name__ == "__main__":
    print(search_flights("Delhi", "Kolkata"))
    print(search_flights("Delhi", "Nowhere"))