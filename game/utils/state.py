from data.mock_api_data import INITIAL_GAME_STATE
from game.models import GameSession, Location
from game.extensions import db

START_CITY = "San Jose" 
# START_CITY_TEST = "Daly City" # test destination reached logic
DESTINATION_CITY = "San Francisco"

# development
def clear_all_games():
    GameSession.query.delete()
    db.session.commit()

def save_game(data):
    db.session.add(data)
    db.session.commit()

def create_new_game():
    start_location = Location.query.filter_by(city_name=START_CITY).first()
    destination_location = Location.query.filter_by(city_name=DESTINATION_CITY).first()

    game = GameSession(
        current_location_id=start_location.id,
        destination_location_id=destination_location.id,
        **INITIAL_GAME_STATE
    )
    db.session.add(game)
    db.session.commit()
    return game

def reset_game(game):
    start_location = Location.query.filter_by(city_name=START_CITY).first()
    destination_location = Location.query.filter_by(city_name=DESTINATION_CITY).first()

    if not start_location or not destination_location:
        raise ValueError("Start or destination location not found")
    
    for field, value in INITIAL_GAME_STATE.items():
        setattr(game, field, value)

    game.current_location_id = start_location.id
    game.destination_location_id = destination_location.id
    db.session.commit()
    return game