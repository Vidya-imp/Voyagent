"""Weather tool using the free Open-Meteo API (no key needed)."""
import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Fog", 51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain", 71: "Light snow", 73: "Snow",
    75: "Heavy snow", 80: "Rain showers", 81: "Rain showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with hail",
}


def _get_coordinates(city: str):
    """Return (latitude, longitude) for a city, or None."""
    response = requests.get(GEOCODE_URL, params={"name": city, "count": 1}, timeout=10)
    response.raise_for_status()
    results = response.json().get("results")
    if not results:
        return None
    return results[0]["latitude"], results[0]["longitude"]


def get_weather(city: str, start_date: str, end_date: str) -> dict:
    """Daily forecast for a city. Dates are 'YYYY-MM-DD'.

    The free forecast only covers about 16 days ahead.
    """
    try:
        coords = _get_coordinates(city)
        if coords is None:
            return {"found": False, "message": f"Could not locate city '{city}'."}
        lat, lon = coords
        params = {
            "latitude": lat, "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
            "timezone": "auto", "start_date": start_date, "end_date": end_date,
        }
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        daily = response.json()["daily"]
        days = [{
            "date": daily["time"][i],
            "condition": WEATHER_CODES.get(daily["weathercode"][i], "Unknown"),
            "max_temp_c": daily["temperature_2m_max"][i],
            "min_temp_c": daily["temperature_2m_min"][i],
            "rain_mm": daily["precipitation_sum"][i],
        } for i in range(len(daily["time"]))]
        return {"found": True, "city": city, "days": days}
    except requests.RequestException as e:
        return {"found": False, "message": f"Weather service error: {e}"}
    except (KeyError, ValueError) as e:
        return {"found": False, "message": f"Unexpected weather response: {e}"}


if __name__ == "__main__":
    from datetime import date, timedelta
    start = date.today() + timedelta(days=2)
    print(get_weather("Delhi", str(start), str(start + timedelta(days=2))))