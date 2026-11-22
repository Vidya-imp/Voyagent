"""LangChain tool wrappers around the plain tool functions."""
from langchain_core.tools import tool

from tools.flight_tool import search_flights
from tools.hotel_tool import recommend_hotels
from tools.places_tool import discover_places, available_place_types
from tools.weather_tool import get_weather
from tools.budget_tool import estimate_budget


@tool
def flight_search(source: str, destination: str, date: str = "",
                  sort_by: str = "cheapest") -> dict:
    """Search flights between two cities. date is optional 'YYYY-MM-DD'.
    sort_by is 'cheapest' or 'fastest'. Returns up to 3 options with price."""
    return search_flights(source, destination, date or None, sort_by)


@tool
def hotel_search(city: str, min_stars: int = 1, max_price_per_night: int = 0) -> dict:
    """Find hotels in a city. min_stars filters by star rating (1-5).
    max_price_per_night of 0 means no limit. Best stars first, then cheapest."""
    return recommend_hotels(city, min_stars, max_price_per_night or None)


@tool
def places_search(city: str, place_type: str = "", min_rating: float = 0.0) -> dict:
    """Find attractions in a city, highest rated first. place_type is optional
    (use place_types_in_city to see valid types)."""
    return discover_places(city, place_type or None, min_rating)


@tool
def place_types_in_city(city: str) -> list:
    """List the attraction types available in a city."""
    return available_place_types(city)


@tool
def weather_forecast(city: str, start_date: str, end_date: str) -> dict:
    """Daily weather forecast for a city. Dates are 'YYYY-MM-DD'.
    Only works for dates within about 16 days from today."""
    return get_weather(city, start_date, end_date)


@tool
def budget_estimate(outbound_flight_price: float, return_flight_price: float,
                    hotel_price_per_night: float, nights: int,
                    daily_expense: float = 1500) -> dict:
    """Estimate total trip cost from the outbound flight price, return flight price,
    hotel price per night and number of nights. Always use this tool for arithmetic
    instead of calculating yourself."""
    return estimate_budget(outbound_flight_price, return_flight_price,
                           hotel_price_per_night, nights, daily_expense)

ALL_TOOLS = [flight_search, hotel_search, places_search, place_types_in_city,
             weather_forecast, budget_estimate]