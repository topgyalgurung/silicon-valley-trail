from game.services.event_service import event_is_allowed

def test_event_is_allowed_when_bugs_is_less_than_min(sample_game):
    sample_game.bugs = 10
    event ={"condition": {"bugs": {"min": 5}}}
    assert event_is_allowed(sample_game, event) == True
