import random

from game.models import GameSession, Location
from game.services.weather_service import get_weather_by_city
from game.utils.utils import get_next_location, clamp_resource, update_game_status, check_coffee_warning, calculate_progress
from game.utils.state import save_game
from data.mock_api_data import EVENTS_BY_LOCATION, ACTION_EFFECTS, COFFEE_WARNING_EVENT, WEATHER_EFFECTS
from game.services.result_types import ActionResult
from game.extensions import db

RESOURCE_FIELDS = ("cash", "morale", "coffee", "hype", "bugs")

def apply_effects(game, effects):
    """Apply effects to game resources using clamp rules"""
    for field in RESOURCE_FIELDS:
        if field not in effects:
            continue
        current_value = getattr(game, field)
        new_value =  current_value + effects[field]
        setattr(game, field, clamp_resource(field, new_value)) # set attr dynamically

def apply_weather_effects(game, weather_data=None):

    weather_data = weather_data or get_weather_by_city(game.current_location.city_name)
    weather = weather_data["summary"]

    effect = WEATHER_EFFECTS.get(weather, {})
    if effect:
        apply_effects(game, effect)
    return weather

def build_api_context(city_name, weather_data=None):
    """
    Normalize API data into a simple structure for event filtering.
    Weather affects which events are eligible, not direct resource changes.
    """
    weather_data = weather_data or get_weather_by_city(city_name)
    return {
        "api_ok": weather_data.get("ok", False),
        "weather_main": weather_data.get("summary"),
        "temperature": weather_data.get("temperature")
    }

def matches_rules(source, rules):
    """Support simple condition rules like min, max, equals, and in."""
    for field, checks in rules.items():
        value = source.get(field)

        if "min" in checks and (value is None or value < checks["min"]):
            return False

        if "max" in checks and (value is None or value > checks["max"]):
            return False

        if "equals" in checks and value != checks["equals"]:
            return False

        if "in" in checks and value not in checks["in"]:
            return False

    return True

def event_matches_condition(event, game, api_context):
    """
    An event is valid only if both:
    1. normal game-state conditions pass
    2. optional API-based conditions pass
    """
    game_state = {
        "cash": game.cash,
        "morale": game.morale,
        "coffee": game.coffee,
        "hype": game.hype,
        "bugs": game.bugs,
        "progress": game.progress,
        "current_day": game.current_day,
    }

    game_condition = event.get("condition", {})
    api_condition = event.get("api_condition", {})

    if game_condition and not matches_rules(game_state, game_condition):
        return False

    if api_condition and not matches_rules(api_context, api_condition):
        return False

    return True

def pick_event_for_location(location_name, game, api_context):
    """pick one valid event for the location"""
    events = EVENTS_BY_LOCATION.get(location_name,[])
    valid_events = [ event for event in events if event_matches_condition(event, game, api_context)]

    if not valid_events:
        return None
    return random.choice(valid_events)

def trigger_event_after_travel(game, next_location, weather_data=None):
    """Trigger one valide eevent after arriving at a new location """
    api_context = build_api_context(next_location.city_name, weather_data)
    event = pick_event_for_location(next_location.city_name, game, api_context)

    game.current_event_key = event["id"] if event else None
    return event 

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

    weather_data = get_weather_by_city(game.current_location.city_name)
    apply_weather_effects(game, weather_data)

    game.current_day += 1
    status, status_message = update_game_status(game)

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

    weather_data = get_weather_by_city(next_location.city_name)
    event = trigger_event_after_travel(game, next_location, weather_data)
    status, status_message = update_game_status(game)
    save_game(game)

    return ActionResult(
        game=game,
        event=event,
        status=status,
        message=status_message,
        game_over=game.status != "in_progress"
    )

def apply_current_event_choice(choice, game):
    """Apply the choice of the current event"""
    if game.current_event_key == "system_coffee_warning":
        option = next((o for o in COFFEE_WARNING_EVENT["options"] if o["id"] == choice), None)
        if not option:
            return ActionResult(
                game=game,
                event=None,
                message=None,
                status=game.status,
                game_over=False,
            )

        effects = option["effect"]
        skip_turns = effects.get("skip_turns", 0)
        game.current_day += skip_turns # add 2 days to current day for 2 coffee skip turns else 1 day

        if choice == "risk_it":
            game.coffee = 0

        apply_effects(game, effects)
        game.current_event_key = None

        status, status_message = update_game_status(game)

        return ActionResult(
            game=game,
            event=None,
            message=status_message or option["text"],
            status=status,
            game_over=status != "in_progress",
        )


    city_events = EVENTS_BY_LOCATION.get(game.current_location.city_name,[])
    event = next((e for e in city_events if e["id"] == game.current_event_key), None)
    if not event:
        return ActionResult(
            game=game,
            event=None,
            message=None,
            status=game.status,
            game_over=False,
        )

    if event.get("requires_input"):
        option = next((o for o in event.get("options", []) if o["id"] == choice), None)
        if not option:
            return ActionResult(
                game=game,
                event=None,
                message=None,
                status=game.status,
                game_over=False,
            )
        effects = option.get("effect", {})
        base_message = option.get("text", None)
    else:
        effects = event.get("effect", {})
        base_message = event.get("text", None)
    
    apply_effects(game, effects)
    game.current_event_key = None
    
    status, status_message = update_game_status(game)

    return ActionResult(
        game=game,
        event=None,
        message=status_message or base_message,
        status=status,
        game_over=status != "in_progress",
    )
    


