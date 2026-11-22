"""Basic tests for the travel agent tools. Run: python -m pytest tests"""
from tools.budget_tool import estimate_budget
from tools.flight_tool import search_flights
from tools.hotel_tool import recommend_hotels
from tools.places_tool import discover_places


def test_budget_total_is_sum_of_parts():
    result = estimate_budget(2907, 2907, 3650, 2)
    assert result["flights"] == 5814
    assert result["hotel"] == 7300
    assert result["food_and_local_travel"] == 4500
    assert result["total"] == 17614


def test_flights_sorted_cheapest_first():
    options = search_flights("Delhi", "Kolkata")["options"]
    prices = [f["price"] for f in options]
    assert prices == sorted(prices)


def test_unknown_route_returns_not_found():
    assert search_flights("Delhi", "Nowhere")["found"] is False


def test_hotels_respect_min_stars():
    for hotel in recommend_hotels("Delhi", min_stars=4)["options"]:
        assert hotel["stars"] >= 4


def test_places_have_no_duplicate_names():
    names = [p["name"] for p in discover_places("Delhi")["options"]]
    assert len(names) == len(set(names))