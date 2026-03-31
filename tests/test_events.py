from game.services.game_service import (
    matches_rules,
    event_matches_condition,
    pick_event_for_location,
)


def test_matches_rules_min():
    source = {"bugs": 5}
    rules = {"bugs": {"min": 3}}

    assert matches_rules(source, rules) is True


def test_matches_rules_equals():
    source = {"weather_main": "Clear"}
    rules = {"weather_main": {"equals": "Clear"}}

    assert matches_rules(source, rules) is True


def test_event_matches_condition_true(sample_game):
    event = {
        "id": "good_weather_bug_fix",
        "condition": {
            "bugs": {"min": 5},
            "morale": {"min": 50},
        },
        "api_condition": {
            "weather_main": {"equals": "Clear"}
        },
    }

    api_context = {
        "weather_main": "Clear",
        "api_ok": True,
        "temperature": 68,
    }

    assert event_matches_condition(event, sample_game, api_context) is True


def test_event_matches_condition_false_when_api_fails(sample_game):
    event = {
        "id": "sunny_only_event",
        "condition": {
            "bugs": {"min": 5}
        },
        "api_condition": {
            "weather_main": {"equals": "Sunny"}
        },
    }

    api_context = {
        "weather_main": "Rain",
        "api_ok": True,
        "temperature": 55,
    }

    assert event_matches_condition(event, sample_game, api_context) is False


def test_pick_event_for_location_returns_none_when_no_valid_event(sample_game, mocker):
    mock_events = {
        "San Jose": [
            {
                "id": "high_bug_event",
                "condition": {"bugs": {"min": 50}},
                "api_condition": {},
            },
            {
                "id": "perfect_weather_event",
                "condition": {},
                "api_condition": {"weather_main": {"equals": "Sunny"}},
            },
        ]
    }

    mocker.patch("game.services.game_service.EVENTS_BY_LOCATION", mock_events)

    api_context = {
        "weather_main": "Rain",
        "api_ok": True,
        "temperature": 60,
    }

    event = pick_event_for_location("San Jose", sample_game, api_context)

    assert event is None