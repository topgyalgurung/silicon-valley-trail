from game.models import Location
from data.mock_api_data import RESOURCE_LIMITS
from game.extensions import db
DESTINATION_CITY = "San Francisco"

def get_next_location(current_location_id):
    current_location = db.session.get(Location, current_location_id)
    if not current_location:
        return None
    return (
        Location.query
        .filter(Location.order_index > current_location.order_index)
        .order_by(Location.order_index)
        .first()
    )

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
    if game.current_location_id == game.destination_location_id:
        game.status = "won"
        return game.status, "You have reached the destination. Let's pitch for your Series A funding! Congratulations!"
    return game.status, None

def check_coffee_warning(game, effects):
    """Return True if coffee warning is triggered"""
    coffee_change = effects.get("coffee", 0)
    if coffee_change >= 0:
        return False
    return game.coffee + coffee_change <=0