import random
from data.mock_api_data import EVENTS_BY_LOCATION

def pick_event_by_location(city, weather):
    """
    Get a random event for a given location. Filter events by weather conditions if applicable.
    """
    city_events = EVENTS_BY_LOCATION.get(city,[])

    if not city_events:
        return None
    # look for events whose weather_conditions match the current weather from weahter api
    weather_matches = [
        e for e in city_events if e.get("weather_conditions") and weather in e["weather_conditions"]
    ]

    if weather_matches:
        return random.choice(weather_matches)
    # if no weather match, pick a random event
    return random.choice(city_events)


    