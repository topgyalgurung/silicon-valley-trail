import pytest
from game.services.weather_service import get_weather_by_city

def test_get_weather_by_city(mocker):

    # mock requests.get
    mock_get = mocker.patch('game.services.weather_service.requests.get')
    mocker.patch('game.services.weather_service.Config.OPENWEATHER_API_KEY', 'test_key')

    # set return values
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ],
        "main": {
            "temp": 30
        }
    }

    # call function
    result = get_weather_by_city("San Jose")

    assert result == {"ok": True, "summary": "Clear", "temperature": 30, "description": "clear sky", "error": None}

    mock_get.assert_called_once_with("https://api.openweathermap.org/data/2.5/weather?q=San Jose&appid=test_key&units=imperial", timeout=10)

def test_get_weather_by_city_falls_back_with_summary(mocker):
    mocker.patch("game.services.weather_service.Config.OPENWEATHER_API_KEY", None)

    result = get_weather_by_city("San Jose")

    assert result["summary"] == "Clear"
    assert "temperature" in result
    assert result["error"] == "missing_api_key"
