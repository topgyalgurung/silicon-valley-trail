from game.models import Location
from game.services.game_service import apply_action


def test_apply_action_triggers_coffee_warning(sample_game, mocker):
    mocker.patch(
        "game.services.game_service.ACTION_EFFECTS",
        {"work": {"coffee": -60}}
    )
    mocker.patch("game.services.game_service.save_game")

    result = apply_action("work", sample_game)

    assert sample_game.current_event_key == "system_coffee_warning"
    assert result.event["id"] == "system_coffee_warning"
    assert result.status == sample_game.status
    assert result.game_over is False


def test_apply_action_non_travel_updates_day_and_resources(sample_game, mocker):
    mocker.patch(
        "game.services.game_service.ACTION_EFFECTS",
        {"work": {"cash": 100, "morale": -5, "coffee": -10}}
    )
    mocker.patch("game.services.game_service.apply_weather_effects", return_value="Clear")
    mocker.patch("game.services.game_service.save_game")

    result = apply_action("work", sample_game)

    assert sample_game.cash == 600
    assert sample_game.morale == 75
    assert sample_game.coffee == 40
    assert sample_game.current_day == 2
    assert sample_game.current_event_key is None
    assert result.event is None
    assert result.game_over is False


def test_apply_action_travel_moves_to_next_location(sample_game, mocker, app):
    current_location = sample_game.current_location
    next_location = Location.query.filter_by(city_name="Santa Clara").first()

    current_location.distance_to_next_miles = 10.0

    mocker.patch(
        "game.services.game_service.ACTION_EFFECTS",
        {"travel": {"coffee": -10}}
    )
    mocker.patch("game.services.game_service.apply_weather_effects", return_value="Clear")
    mocker.patch("game.services.game_service.trigger_event_after_travel", return_value=None)
    mocker.patch("game.services.game_service.save_game")

    result = apply_action("travel", sample_game)

    assert sample_game.current_day == 2
    assert sample_game.current_location_id == next_location.id
    assert sample_game.distance_traveled_miles == 10.0
    assert sample_game.progress >= 0
    assert result.event is None
    assert result.game_over is False


def test_apply_action_travel_wins_when_no_next_location(sample_game, mocker):
    destination = sample_game.destination_location
    sample_game.current_location_id = destination.id

    mocker.patch(
        "game.services.game_service.ACTION_EFFECTS",
        {"travel": {"coffee": -10}}
    )
    mocker.patch("game.services.game_service.apply_weather_effects", return_value="Clear")
    mocker.patch("game.services.game_service.get_next_location", return_value=None)
    mocker.patch("game.services.game_service.save_game")

    result = apply_action("travel", sample_game)

    assert sample_game.status == "won"
    assert result.status == "won"
    assert result.game_over is True