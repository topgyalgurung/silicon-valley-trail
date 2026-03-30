from game.services.event_service import event_is_allowed, pick_event_by_location

def test_event_is_allowed_when_bugs_is_less_than_min(sample_game):
    sample_game.bugs = 10
    event ={"condition": {"bugs": {"min": 5}}}
    assert event_is_allowed(sample_game, event) == True


def test_event_allowed_when_no_condition(sample_game):
    sample_game.bugs = 2
    event = {"condition": {"bugs": {"min": 5}}}
    assert event_is_allowed(sample_game, event) == False

def test_pick_event_by_location_weather_match(sample_game, mocker):
    mocker.patch('game.services.event_service.random.choice', side_effect=lambda x: x[0]) # return the first element of the list
    event = pick_event_by_location("Santa Clara", "Rain", sample_game) # returns event as a dictionary
    assert event['id'] == "sc_rain_commute"

def test_pick_event_returns_random_when_no_weather_match(sample_game, mocker):
    mocker.patch('game.services.event_service.random.choice',
                 side_effect=lambda x: x[0])
    event = pick_event_by_location("Santa Clara", "Sunny", sample_game)
    assert event is not None