from game.services.game_service import update_game_status
from game.models import Location

def test_game_loses_when_cash_reaches_zero(sample_game):
    sample_game.cash = 0
    game_status,message = update_game_status(sample_game)
    assert game_status == "lost"
    assert sample_game.status == "lost"


def test_game_loses_when_morale_reaches_zero(sample_game):
    sample_game.morale = 0
    game_status, message = update_game_status(sample_game)
    assert game_status == "lost"
    assert sample_game.status == "lost"


def test_game_wins_when_reaching_destination(sample_game):
    destination = Location.query.filter_by(city_name="San Francisco").first()
    sample_game.current_location_id = destination.id
    message = update_game_status(sample_game)
    assert sample_game.status == "won"


def test_cash_at_one_still_shows_in_progress(sample_game):
    sample_game.cash = 1
    game_status, message = update_game_status(sample_game)
    assert game_status == "in_progress"
    assert message is None

