# business logic 

from asyncio import Event
import random
from data.game_data import EVENTS_BY_LOCATION, ACTION_EFFECTS
from game.models import GameSession, Location
from game.extensions import db


def save_game(game):
    # commit state to database
    db.session.commit()
    return game

def get_next_location(current_location_id):
    return Location.query.filter(Location.order_index > current_location_id).order_by(Location.order_index).first()

def update_game_status(game):

    if game.coffee == 0:
        game.coffee_zero_turns += 1
    if game.coffee_zero_turns >= 2:
        game.status = "lost"
        save_game(game)
        return game, None, "You have run out of coffee"
    if game.morale <= 0:
        game.status = "lost"
        save_game(game)
        return game, None, "Your morale has collapsed"
    if game.cash <= 0:
        game.status = "lost"
        save_game(game)
        return game, None, "You have run out of cash"
    if game.progress >= 100:
        game.status = "won"
        save_game(game)
        return game, None, "You have reached the destination"
    return game, None, None

def apply_effects(game, effects):
    resource_fields = ("cash", "morale", "coffee", "hype", "bugs", "progress")
    for field in resource_fields:
        if field in effects:
            setattr(game, field, getattr(game, field) + effects[field])


def apply_action(action, game):
    effects = ACTION_EFFECTS.get(action, {})
    event = None 
    apply_effects(game, effects)

    if action == "travel":
        next_location = get_next_location(game.current_location_id)
        if not next_location:
            save_game(game)
            return game,None,"You have reached the destination"
        game.current_location_id = next_location.id
        game.current_day += 1

        events = EVENTS_BY_LOCATION.get(next_location.city_name,[])
        event = random.choice(events) if events else None # todo: add a weighted random choice based on the event's probability
        game.current_event_key = event["key"] if event else None
    else:
        game.current_event_key = None
    save_game(game)
    return game, event

def apply_current_event_choice(choice, game):
    city_events = EVENTS_BY_LOCATION.get(game.current_location.city_name,[])
    event = next((e for e in city_events if e["key"] == game.current_event_key), None)
    if not event:
        return game, None
    if event.get("requires_input"):
        option = next((o for o in event.get("options", []) if o["id"] == choice), None)
        effects = option.get("effect", {})
    else:
        effects = event.get("effects", {})
    apply_effects(game, effects)

    message = effects.get("message")
    game.current_event_key = None

    save_game(game)
    return game, message



