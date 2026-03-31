import random
from data.mock_api_data import EVENTS_BY_LOCATION

def event_is_allowed(game, event):
    """Return True if event is allowed based on game state"""
    condition = event.get("condition", {})
    bugs_rule = condition.get("bugs", {})
    if bugs_rule:
        if game.bugs < bugs_rule.get("min", 0):
            return False
    return True

def pick_event_by_location(city, weather, game):
    """
    Get a random event for a given location. 
    """
    city_events = EVENTS_BY_LOCATION.get(city,[])
    if not city_events:
        return None

    # filter events by condition
    valid_events = [e for e in city_events if event_is_allowed(game, e)]
    if not valid_events:
        return None

    # look for events whose weather_conditions match the current weather from weather api
    weather_matches = [
        e for e in city_events if e.get("weather_conditions") and weather in e["weather_conditions"]
    ]

    if weather_matches:
        return random.choice(weather_matches)
    return random.choice(city_events)
