from data.mock_api_data import INITIAL_GAME_STATE
from game.models import GameSession, Location
from game.utils.utils import get_start_and_destination_locations
from game.extensions import db


# development
def clear_all_games():
    GameSession.query.delete()
    db.session.commit()

def save_game(data):
    db.session.add(data)
    db.session.commit()

def create_new_game():
    start_location, destination_location = get_start_and_destination_locations()

    game = GameSession(
        current_location_id=start_location.id,
        destination_location_id=destination_location.id,
        **INITIAL_GAME_STATE
    )
    db.session.add(game)
    db.session.commit()
    return game

def reset_game(game):
    start_location, destination_location = get_start_and_destination_locations()
    
    for field, value in INITIAL_GAME_STATE.items():
        setattr(game, field, value)

    game.current_location_id = start_location.id
    game.destination_location_id = destination_location.id
    db.session.commit()
    return game