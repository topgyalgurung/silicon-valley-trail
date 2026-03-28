from game.extensions import db
from game.models import GameSession, Location

def create_new_game():
    start_location = Location.query.filter_by(city_name="San Jose").first()
    destination_location = Location.query.filter_by(city_name="San Francisco").first()
    # create fresh game session with initial state
    game = GameSession(
        current_day=1,
        current_location_id=start_location.id,
        destination_location_id=destination_location.id,
        status= "in_progress",
        cash=50000, 
        morale=100, # 0-100
        coffee=50, # if stays 0 for 2 turn -> lose
        hype=50,  # 0-100
        bugs=0,
        progress=0, # 0-100
        coffee_zero_turns=0,
        current_event_key=None,
    )
    db.session.add(game)
    db.session.commit()
    return game