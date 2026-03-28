# business logic 

from asyncio import Event
import random
from data.mock_api_data import INITIAL_GAME_STATE, EVENTS_BY_LOCATION, ACTION_EFFECTS
from game.models import GameSession, Location
from game.services.event_service import pick_event_by_location
from game.services.weather_service import get_weather_by_city
from game.extensions import db

def create_new_game():
    start_location = Location.query.filter_by(city_name="San Jose").first()
    destination_location = Location.query.filter_by(city_name="San Francisco").first()
    # create fresh game session with initial state
    game = GameSession(
        current_location_id=start_location.id,
        destination_location_id=destination_location.id,
        **INITIAL_GAME_STATE
    )
    db.session.add(game)
    db.session.commit()
    return game

def reset_game(game):
    start_location = Location.query.filter_by(city_name="San Jose").first()
    destination_location = Location.query.filter_by(city_name="San Francisco").first()

    if not start_location or not destination_location:
        raise ValueError("Start or destination location not found")
    
    for field, value in INITIAL_GAME_STATE.items():
        setattr(game, field, value)

    game.current_location_id = start_location.id
    game.destination_location_id = destination_location.id
    db.session.commit()
    return game

def save_game(data):
    # commit state to database
    db.session.add(data)
    db.session.commit()

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

def handle_travel(game, next_location):
    weather_data = get_weather_by_city(next_location.city_name)
    weather_summary = weather_data["summary"]

    event = pick_event_by_location(next_location.city_name, weather_summary)
    if event:
        game.current_event_key = event["id"]
        return event
    events = EVENTS_BY_LOCATION.get(next_location.city_name,[])
    event = random.choice(events) if events else None # todo: add a weighted random choice based on the event's probability
    game.current_event_key = event["id"] if event else None
    return event


def apply_effects(game, effects):
    resource_fields = ("cash", "morale", "coffee", "hype", "bugs", "progress")
    for field in resource_fields:
        if field in effects:
            setattr(game, field, getattr(game, field) + effects[field])


def apply_action(action, game):
    effects = ACTION_EFFECTS.get(action, {})
    apply_effects(game, effects)

    next_location = get_next_location(game.current_location_id)
    if not next_location:
        save_game(game)
        return game,None
    game.current_location_id = next_location.id
    game.current_day += 1

    if action!="travel":
        game.current_event_key = None
        save_game(game)
        return game, None
    print(f"next_location type: {type(next_location)}, value: {next_location}")
    event = handle_travel(game, next_location)
    save_game(game)
    return game, event

def apply_current_event_choice(choice, game):
    city_events = EVENTS_BY_LOCATION.get(game.current_location.city_name,[])
    event = next((e for e in city_events if e["id"] == game.current_event_key), None)
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



