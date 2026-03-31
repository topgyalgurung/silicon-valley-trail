import random

from game.models import GameSession, Location
from game.services.event_service import pick_event_by_location
from game.services.weather_service import get_weather_by_city
from game.utils.utils import get_next_location, clamp_resource, update_game_status, check_coffee_warning, calculate_progress
from game.utils.state import save_game
from data.mock_api_data import EVENTS_BY_LOCATION, ACTION_EFFECTS, COFFEE_WARNING_EVENT, WEATHER_EFFECTS
from game.services.result_types import ActionResult
from game.extensions import db

RESOURCE_FIELDS = ("cash", "morale", "coffee", "hype", "bugs")

def apply_effects(game, effects):
    """Apply effects to game resources and update derived fields like progress"""
    for field in RESOURCE_FIELDS:
        if field not in effects:
            continue
        current_value = getattr(game, field)
        new_value =  current_value + effects[field]
        setattr(game, field, clamp_resource(field, new_value)) # set attr dynamically

def apply_weather_effects(game):

    weather_data = get_weather_by_city(game.current_location.city_name)
    weather = weather_data["summary"]

    effect = WEATHER_EFFECTS.get(weather, {})
    if effect:
        apply_effects(game, effect)
    return weather

def apply_action(action, game):
    effects = ACTION_EFFECTS.get(action, {})

    # if game coffee == effect then trigger coffee warning to replenish
    if check_coffee_warning(game, effects):
        game.current_event_key = COFFEE_WARNING_EVENT["id"]
        save_game(game)
        return ActionResult(
            game=game,
            event=COFFEE_WARNING_EVENT,
            status=game.status,
            message=None,
            game_over=False
        )

    apply_effects(game, effects)

    # real time weather effects apply
    weather = apply_weather_effects(game)

    game.current_day += 1
    _, status_message = update_game_status(game)

    if game.status != "in_progress":
        return ActionResult(
            game=game,
            event=None,
            status=game.status,
            message=status_message,
            game_over=True
        )

    if action != "travel":
        game.current_event_key = None
        save_game(game)
        return ActionResult(
            game=game,
            event=None,
            message=None,
            status=game.status,
            game_over=False
        )

    # travel logic
    current_location = db.session.get(Location, game.current_location_id)
    next_location = get_next_location(game.current_location_id)

    if not next_location:
        game.status = "won"
        save_game(game)
        return ActionResult(
            game=game,
            event=None,
            status=game.status,
            progress=game.progress,
            message="Congratulations, you reached San Francisco!",
            game_over=True
        )
    # for progress percentage
    segment_distance = current_location.distance_to_next_miles or 0.0
    game.distance_traveled_miles += segment_distance # distance traveled so far
    game.progress = calculate_progress(game.distance_traveled_miles)

    game.current_location_id = next_location.id

    event = handle_travel(game, next_location)
    status, status_message = update_game_status(game)
    save_game(game)

    return ActionResult(
        game=game,
        event=event,
        status=status,
        message=status_message,
        game_over=game.status != "in_progress"
    )

def handle_travel(game, next_location):
    weather_data = get_weather_by_city(next_location.city_name)
    weather_summary = weather_data["summary"]

    event = pick_event_by_location(next_location.city_name, weather_summary, game)
    
    if not event: 
        events = EVENTS_BY_LOCATION.get(next_location.city_name,[])
        event = random.choice(events) if events else None # todo: add a weighted random choice based on the event's probability

    game.current_event_key = event["id"] if event else None
    return event 

def apply_current_event_choice(choice, game):
    """Apply the choice of the current event"""
    if game.current_event_key == "system_coffee_warning":
        option = next((o for o in COFFEE_WARNING_EVENT["options"] if o["id"] == choice), None)
        if not option:
            return game, None

        effects = option["effect"]
        skip_turns = effects.get("skip_turns", 0)
        game.current_day += skip_turns # add 2 days to current day for 2 coffee skip turns else 1 day

        if choice == "risk_it":
            game.coffee = 0

        apply_effects(game, effects)
        return game, option["text"]

    city_events = EVENTS_BY_LOCATION.get(game.current_location.city_name,[])
    event = next((e for e in city_events if e["id"] == game.current_event_key), None)
    if not event:
        return game, None

    if event.get("requires_input"):
        option = next((o for o in event.get("options", []) if o["id"] == choice), None)
        effects = option.get("effect", {})
    else:
        effects = event.get("effect", {})

    apply_effects(game, effects)
    message = effects.get("message")
    game.current_event_key = None
    return game, message
    


