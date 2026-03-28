# business logic 

import random
from data.game_data import EVENTS_BY_LOCATION
from game.models import GameSession, Location
from game.extensions import db


def save_game(game):
    # commit state to database
    db.session.commit()
    return game
    
def get_next_location(current_location_id):
    return Location.query.filter(Location.order_index > current_location_id).order_by(Location.order_index).first()

def apply_action(action, game):
    # check if action is valid
    # check if win or lose conditions are met
    # event interuption random 

    if action == "travel":
        next_location = get_next_location(game.current_location_id)
        if not next_location:
            return game,None,"You have reached the destination"
        game.current_location_id = next_location.id
        game.current_day += 1
        game.progress += 1 # todo: calculate progress based on distance between current and destination locations
        game.cash = game.cash - 1000 # gas cost 
        game.coffee = game.coffee - 10
        game.current_event_key = "travel"

        events = EVENTS_BY_LOCATION.get(next_location.city_name,[])
        event = random.choice(events) if events else None # todo: add a weighted random choice based on the event's probability
        game.current_event_key = event["key"] if event else None
        save_game(game)
        return game, event

def calculate_event_outcome(choice, game):
    city_events = EVENTS_BY_LOCATION.get(game.current_location.city_name,[])
    event = next((e for e in city_events if e["key"] == game.current_event_key), None)
    if not event:
        return game, None, "No event found"
    
    outcome = event.get("outcomes", {}).get(choice, {})
    if not outcome:
        return game, None, "No outcome found"

    game.cash += outcome.get("cash", 0)
    game.morale += outcome.get("morale", 0)
    game.coffee += outcome.get("coffee", 0)
    game.hype += outcome.get("hype", 0)
    game.bugs += outcome.get("bugs", 0)
    return game, event, outcome.get("message", "")
