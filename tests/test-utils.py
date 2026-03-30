from game.utils import clamp_resource

def test_clamp_resource():
    assert clamp_resource("cash", 1000) == 1000
    assert clamp_resource("cash", -1000) == 0
    assert clamp_resource("morale", 100) == 100
    assert clamp_resource("morale", -100) == 0
    assert clamp_resource("morale", 150) == 100
    assert clamp_resource("coffee", 50) == 50
    assert clamp_resource("coffee", -100) == 0
    assert clamp_resource("hype", 50) == 50
    assert clamp_resource("hype", -1) == 0
    assert clamp_resource("hype", 150) == 100
    assert clamp_resource("bugs", -1) == 0
