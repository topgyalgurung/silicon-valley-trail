from game.models import Location
from data.mock_api_data import RESOURCE_LIMITS
DESTINATION_CITY = "San Francisco"

def get_total_distance_miles():
    locations = Location.query.order_by(Location.order_index.asc()).all()
    return sum(location.distance_to_next_miles or 0.0 for location in locations)

def get_next_location(current_location_id):
    current_location = Location.query.get(current_location_id)
    if not current_location:
        return None
    return Location.query.filter(Location.order_index > current_location.order_index).order_by(Location.order_index).first()

def calculate_progress(distance_traveled_miles):
    total_distance_miles = get_total_distance_miles()

    if total_distance_miles == 0:
        return 0
    return format((distance_traveled_miles / total_distance_miles) * 100, ".0f")


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


# def apply_resource_change(game, resource_name, change):
#     current_value = getattr(game, resource_name)
#     new_value = current_value + change

#     limits = RESOURCE_LIMITS[resource_name]
#     new_value = clamp_resource(new_value, limits["min"], limits["max"])

#     setattr(game, resource_name, new_value)

def evaluate_game_status(game):
    """return user facing status message if game is won, lost, coffee zero turns"""
    if game.morale <= 0:
        game.status = "lost"
        return game.status, "You have lost the game. Your morale has collapsed"
    if game.cash <= 0:
        game.status = "lost"
        return game.status, "You have run out of cash. Game over. "
    # if game.progress >= 100: # first need to calculate progress in percentage
    #     game.status = "won"
    #     return "You made it to the destination. Congratulations!"
    game.status = "in_progress" # might not need this revisit later might have already handled
    return game.status, None

def check_coffee_warning(game, effects):
    """Return True if coffee warning is triggered"""
    coffee_change = effects.get("coffee", 0)
    if coffee_change >= 0:
        return False
    else:
        return game.coffee + coffee_change <=0