# business logic 

from asyncio import Event
import random
from data.mock_api_data import INITIAL_GAME_STATE, EVENTS_BY_LOCATION, ACTION_EFFECTS, RESOURCE_LIMITS, COFFEE_WARNING_EVENT
from game.models import GameSession, Location
from game.services.event_service import pick_event_by_location
from game.services.weather_service import get_weather_by_city
from game.extensions import db
from game.utils import get_next_location, clamp_resource, evaluate_game_status, check_coffee_warning
from game.services.result_types import ActionResult

START_CITY = "San Jose"
DESTINATION_CITY = "San Francisco"
RESOURCE_FIELDS = ("cash", "morale", "coffee", "hype", "bugs", "progress")

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

def save_game(data):
    # commit state to database
    db.session.add(data)
    db.session.commit()


def handle_travel(game, next_location):
    weather_data = get_weather_by_city(next_location.city_name)
    weather_summary = weather_data["summary"]

    event = pick_event_by_location(next_location.city_name, weather_summary)
    
    if not event: 
        events = EVENTS_BY_LOCATION.get(next_location.city_name,[])
        event = random.choice(events) if events else None # todo: add a weighted random choice based on the event's probability

    game.current_event_key = event["id"] if event else None
    return event # might return weather also here revisit later


def apply_effects(game, effects):
    """Apply effects to game resources and update derived fields like progress"""
    for field in RESOURCE_FIELDS:
        if field not in effects:
            continue
        current_value = getattr(game, field)
        print(f"current_value: {current_value}, field: {field}")
        new_value =  current_value + effects[field]
        updated_value = clamp_resource(field, new_value)
        setattr(game, field, updated_value) # setattr(game, field, new_value)
        print(f"updated_value: {updated_value}, field: {field}") # test
    if game.coffee == 0:
        game.current_day += 2


def apply_action(action, game):
    print(f"applying action: {action} to game")
    effects = ACTION_EFFECTS.get(action, {})

    # check for coffee warning 
    if check_coffee_warning(game, effects):
        game.current_event_key = COFFEE_WARNING_EVENT["id"]
        save_game(game)
        return ActionResult(
            game = game, 
            event = COFFEE_WARNING_EVENT,
            status = game.status,
            message = None,
            game_over = False
        )
    apply_effects(game, effects)

    game.current_day += 1 # increment day on all actions
    status_message = evaluate_game_status(game)

    if game.status != "in_progress":
        return ActionResult(
            game=game,
            event=None,
            status=game.status,
            message= status_message,
            game_over=True
        )

    if action!="travel":
        game.current_event_key = None
        save_game(game)
        return ActionResult(
            game=game,
            event=None,
            message=None,
            status=game.status,
            game_over=False
        )
    next_location = get_next_location(game.current_location_id)
    if not next_location:
        game.status = "won"
        save_game(game) # save game to see resources after winning
        return ActionResult(
            game=game,
            status="won",
            message="You made it to the destination. Congratulations!",
            game_over=True
        )
    game.current_location_id = next_location.id # update current location

    event = handle_travel(game, next_location)
    status_message = evaluate_game_status(game) # check after travel events choices effects on game status
    save_game(game)
    return ActionResult(
        game=game,
        event=event,
        status=game.status,
        message=status_message,
        game_over=False
    )

def apply_current_event_choice(choice, game):
    
    if game.current_event_key == "system_coffee_warning":
        option = next((o for o in COFFEE_WARNING_EVENT["options"] if o["id"] == choice), None)
        effects = option["effect"]

        skip_turns = effects.pop("skip_turns", 0)
        game.current_day += skip_turns # add 2 days to current day for 2 skip turns 

        apply_effects(game, effects)
        save_game(game)
        return game, option["text"]

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



