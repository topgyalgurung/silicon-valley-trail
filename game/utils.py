from game.models import Location

def get_total_distance_miles():
    locations = Location.query.order_by(Location.order_index.asc()).all()
    return sum(location.distance_to_next_miles or 0.0 for location in locations)

def get_next_location(current_location_id):
    return Location.query.filter(Location.order_index > current_location_id).order_by(Location.order_index).first()

def calculate_progress(distance_traveled_miles):
    total_distance_miles = get_total_distance_miles()

    if total_distance_miles == 0:
        return 0
    return format((distance_traveled_miles / total_distance_miles) * 100, ".0f")