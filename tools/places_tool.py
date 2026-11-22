"""Places / attractions discovery tool."""
from utils import load_json, same_text


def discover_places(city: str, place_type: str = None, min_rating: float = 0.0,
                    limit: int = 10) -> dict:
    """Find attractions in a city, highest rated first.

    place_type is optional (e.g. 'temple', 'lake', 'beach').
    """
    places = [p for p in load_json("places.json")
              if same_text(p["city"], city) and p["rating"] >= min_rating]
    if place_type:
        places = [p for p in places if same_text(p["type"], place_type)]

    # --- NEW: keep only the highest-rated entry for each place name ---
    best_by_name = {}
    for place in places:
        name = place["name"].strip().lower()
        if name not in best_by_name or place["rating"] > best_by_name[name]["rating"]:
            best_by_name[name] = place
    places = list(best_by_name.values())
    # --- end of new block ---

    if not places:
        return {"found": False, "message": f"No places match in {city}.", "options": []}

    places.sort(key=lambda p: -p["rating"])
    return {"found": True, "options": places[:limit]}


def available_place_types(city: str) -> list:
    """List the place types available in a city."""
    return sorted({p["type"] for p in load_json("places.json") if same_text(p["city"], city)})


if __name__ == "__main__":
    print(discover_places("Delhi", min_rating=4.0, limit=5))
    print(available_place_types("Delhi"))