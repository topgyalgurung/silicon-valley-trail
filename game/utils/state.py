from data.mock_api_data import INITIAL_GAME_STATE
from game.models import GameSession, Location
from game.utils.utils import get_start_and_destination_locations
from game.extensions import db


# development
def clear_all_games():
    GameSession.query.delete()
    db.session.commit()

def save_game(game):
    
    new_game_state = GameSession(
        current_day=game.current_day,
        current_location_id=game.current_location_id,
        destination_location_id=game.destination_location_id,
        status=game.status,
        progress=game.progress,
        distance_traveled_miles=game.distance_traveled_miles,
        current_event_key=game.current_event_key,
        cash=game.cash,
        morale=game.morale,
        coffee=game.coffee,
        hype=game.hype,
        bugs=game.bugs,
        missed_coffee_turns=game.missed_coffee_turns,
    )
    db.session.add(new_game_state)
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