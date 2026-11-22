def estimate_budget(outbound_flight_price: float, return_flight_price: float,
                    hotel_price_per_night: float, nights: int,
                    daily_expense: float = 1500) -> dict:
    """Total = outbound flight + return flight + hotel + daily food/local travel.

    Food and local travel is charged for (nights + 1) days.
    """
    flight_cost = outbound_flight_price + return_flight_price
    hotel_cost = hotel_price_per_night * nights
    days = nights + 1
    local_cost = daily_expense * days
    return {
        "flights": flight_cost,
        "hotel": hotel_cost,
        "food_and_local_travel": local_cost,
        "days_counted_for_food": days,
        "total": flight_cost + hotel_cost + local_cost,
    }


if __name__ == "__main__":
    print(estimate_budget(2907, 2907, 3650, 2))  # expect total 17614