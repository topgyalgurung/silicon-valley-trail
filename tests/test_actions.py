from game.services.game_service import apply_effects, apply_current_event_choice
from game.utils.utils import check_coffee_warning

# sample game has cash=500, morale=80, coffee=50, hype=40, bugs=10, progress=0

def test_apply_effects_multiple_fields(sample_game):
    effects = {"cash": -100, "morale": 10, "coffee": -20, "hype": 15, "bugs": -5}
    apply_effects(sample_game, effects)
    assert sample_game.cash == 400
    assert sample_game.morale == 90
    assert sample_game.coffee == 30
    assert sample_game.hype == 55
    assert sample_game.bugs == 5

def test_apply_effects_clamps_resources(sample_game):
    effects = {"morale": -999, "coffee": -999, "hype": 200, "bugs": -999}
    apply_effects(sample_game, effects)
    assert sample_game.morale == 0
    assert sample_game.coffee == 0
    assert sample_game.hype == 100
    assert sample_game.bugs == 0

def test_check_coffee_warning(sample_game):
    sample_game.coffee = 50
    effects = {"coffee": -10}
    assert check_coffee_warning(sample_game, effects) == False

def test_check_coffee_warning_triggers(sample_game):
    sample_game.coffee = 5
    effects = {"coffee": -10}
    assert check_coffee_warning(sample_game, effects) == True

def test_apply_current_event_choice_system_warning_valid(sample_game, mocker):
    sample_game.current_event_key = "system_coffee_warning"

    mock_coffee_warning_event = {
        "id": "system_coffee_warning",
        "options": [
            {
                "id": "buy_coffee",
                "text": "Buy coffee",
                "effect": {"cash": -50, "coffee": 20}
            },
            {
                "id": "risk_it",
                "text": "Risk it",
                "effect": {"skip_turns": 2, "morale": -10}
            },
        ],
    }

    mocker.patch(
        "game.services.game_service.COFFEE_WARNING_EVENT",
        mock_coffee_warning_event
    )

    result = apply_current_event_choice("buy_coffee", sample_game)

    assert result.game.cash == 450
    assert result.game.coffee == 70
    assert result.game.current_day == 1
    assert result.message == "Buy coffee"


def test_apply_current_event_choice_system_warning_invalid(sample_game, mocker):
    sample_game.current_event_key = "system_coffee_warning"

    mock_coffee_warning_event = {
        "id": "system_coffee_warning",
        "options": [
            {
                "id": "buy_coffee",
                "text": "Buy coffee",
                "effect": {"cash": -50, "coffee": 20}
            }
        ],
    }

    mocker.patch(
        "game.services.game_service.COFFEE_WARNING_EVENT",
        mock_coffee_warning_event
    )

    result = apply_current_event_choice("invalid_choice", sample_game)

    assert result.game == sample_game
    assert result.game.cash == 500
    assert result.game.coffee == 50
    assert result.message is None


def test_apply_current_event_choice_city_event_with_input(sample_game, mocker):
    sample_game.current_event_key = "coffee_cart"

    mock_events = {
        "San Jose": [
            {
                "id": "coffee_cart",
                "requires_input": True,
                "options": [
                    {
                        "id": "buy",
                        "text": "Buy coffee",
                        "effect": {"cash": -50, "coffee": 20}
                    },
                    {
                        "id": "skip",
                        "text": "Skip it",
                        "effect": {"morale": -5}
                    },
                ],
            }
        ]
    }

    mocker.patch(
        "game.services.game_service.EVENTS_BY_LOCATION",
        mock_events
    )

    result = apply_current_event_choice("buy", sample_game)

    assert result.game.cash == 450
    assert result.game.coffee == 70
    assert result.game.current_event_key is None
    assert result.message == "Buy coffee"


def test_apply_current_event_choice_city_event_without_input(sample_game, mocker):
    sample_game.current_event_key = "rain_commute"

    mock_events = {
        "San Jose": [
            {
                "id": "rain_commute",
                "requires_input": False,
                "effect": {"coffee": -10, "morale": -5},
                "text": "Rain slows the team",
            }
        ]
    }

    mocker.patch(
        "game.services.game_service.EVENTS_BY_LOCATION",
        mock_events
    )

    result = apply_current_event_choice("anything", sample_game)

    assert result.game.coffee == 40
    assert result.game.morale == 75
    assert result.game.current_event_key is None
    assert result.message == "Rain slows the team"