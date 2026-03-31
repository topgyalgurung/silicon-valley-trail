from game.utils.utils import clamp_resource, calculate_progress

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

def test_calculate_progress_returns_expected_percent(mocker):
    # mock total distance to 100 miles
    mocker.patch(
        "game.utils.utils.get_total_distance_miles",
        return_value=100
    )

    result = calculate_progress(25)

    assert result == 25  # (25 / 100) * 100


def test_calculate_progress_caps_at_100(mocker):
    # mock total distance to 100 miles
    mocker.patch(
        "game.utils.utils.get_total_distance_miles",
        return_value=100
    )

    result = calculate_progress(150)

    assert result == 100  # should not exceed 100