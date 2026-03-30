from game.models import Location
from data.mock_api_data import RESOURCE_LIMITS
from game.extensions import db
from game.services.weather_service import get_weather_by_city
DESTINATION_CITY = "San Francisco"

def get_next_location(current_location_id):
    current_location = db.session.get(Location, current_location_id)
    if not current_location:
        return None
    next_order = current_location.order_index + 1
    return Location.query.filter(Location.order_index == next_order).first()

def clamp_resource(field, new_value):
    """keep resource within allowed limits before updating"""
    limits = RESOURCE_LIMITS.get(field, {})
    min_value = limits.get("min", None)
    max_value = limits.get("max", None)
    value = new_value
    if min_value is not None:
        value = max(min_value, new_value)
    if max_value is not None:
        value = min(max_value, value)
    return value

def evaluate_game_status(game):
    """ check win loss conditions and update game.status """
    if game.morale <= 0:
        game.status = "lost"
        return game.status, "You have lost the game. Your morale has collapsed"
    if game.cash <= 0:
        game.status = "lost"
        return game.status, "You have run out of cash. Game over. "
    if game.current_day >= 20 and game.current_location_id != game.destination_location_id:
        game.status = "lost"
        return game.status, "You have not reached the destination in 20 days to pitch for your Series A funding. Game over. "
    if game.current_location_id == game.destination_location_id:
        game.status = "won"
        return game.status, "Congratulations,You have reached San Francisco. Let's pitch for your Series A funding!"
    return game.status, None

def check_coffee_warning(game, effects):
    """Return True if coffee warning is triggered"""
    coffee_change = effects.get("coffee", 0)
    if coffee_change >= 0:
        return False
    return game.coffee + coffee_change <=0

def get_game_weather(game):
    weather_data = get_weather_by_city(game.current_location.city_name)
    weather_warning = None
    if not weather_data["ok"]:
        weather_warning = "live weather unavailable. Showing fallback data."
    return weather_data, weather_warning


def get_total_distance_miles():
    locations = Location.query.order_by(Location.order_index.asc()).all()
    return sum(location.distance_to_next_miles or 0.0 for location in locations)

def calculate_progress(distance_traveled_miles):
    total_distance_miles = get_total_distance_miles()

    if total_distance_miles == 0:
        return 0.0
    percentage = (distance_traveled_miles / total_distance_miles) * 100 
    return round(min(100.0, percentage), 2)