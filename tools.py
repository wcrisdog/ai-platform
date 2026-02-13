def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for flights between origin and destination on a specific date."""
    return (
        f"Found flights from {origin} to {destination} on {date}: "
        "Flight A123 ($300), Flight B456 ($350)."
    )


def book_flight(flight_id: str, passenger_name: str) -> str:
    """Book a specific flight. REQUIRES USER CONFIRMATION FIRST."""
    return f"Successfully booked flight {flight_id} for {passenger_name}."


def search_hotels(location: str, check_in_date: str) -> str:
    """Search for hotels in a specific location."""
    return (
        f"Found hotels in {location} for {check_in_date}: "
        "Hotel Paradise ($100/night), City Inn ($80/night)."
    )


def book_hotel(hotel_name: str, number_of_nights: int) -> str:
    """Book a specific hotel. REQUIRES USER CONFIRMATION FIRST."""
    return f"Successfully booked {hotel_name} for {number_of_nights} nights."


def search_attractions(location: str) -> str:
    """Search for attractions or scenic spots in a location."""
    return f"Top attractions in {location}: Ancient Temple, City Museum, National Park."


def book_attraction(attraction_name: str, number_of_tickets: int) -> str:
    """Book tickets for an attraction. REQUIRES USER CONFIRMATION FIRST."""
    return f"Successfully booked {number_of_tickets} tickets for {attraction_name}."
