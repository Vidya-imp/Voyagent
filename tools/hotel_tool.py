"""Hotel recommendation tool."""
from utils import load_json, same_text


def recommend_hotels(city: str, min_stars: int = 1, max_price_per_night: int = None,
                     limit: int = 3) -> dict:
    """Find hotels in a city, best stars first, then cheapest."""
    hotels = [h for h in load_json("hotels.json")
              if same_text(h["city"], city) and h["stars"] >= min_stars]
    if max_price_per_night is not None:
        hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    if not hotels:
        return {"found": False, "message": f"No hotels match in {city}.", "options": []}

    hotels.sort(key=lambda h: (-h["stars"], h["price_per_night"]))
    return {"found": True, "options": hotels[:limit]}


if __name__ == "__main__":
    print(recommend_hotels("Delhi", min_stars=4))