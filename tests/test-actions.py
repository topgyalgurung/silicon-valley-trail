from random import sample
from game.services.game_service import apply_effects
from game.utils import clamp_resource
from types import SimpleNamespace

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



