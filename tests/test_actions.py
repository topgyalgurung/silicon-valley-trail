from random import sample
from game.services.game_service import apply_effects
from game.utils.utils import check_coffee_warning
from game.services.game_service import apply_current_event_choice

# sample game has cash=500, morale=80, coffee=50, hype=50, bugs=0, progress=0

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




