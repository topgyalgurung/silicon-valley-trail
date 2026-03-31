import requests
import logging
from game.config import Config
from data.mock_api_data import MOCK_WEATHER

logger = logging.getLogger(__name__)

DEFAULT_WEATHER_DATA = {
    "ok": False,
    "summary": "Clear",
    "temperature": 30,
    "description": "clear sky",
    "error": "unavailable"
}
# TODO: cache weather data for few api calls, faster page loads 

def get_weather_by_city(city_name):
    api_key = Config.OPENWEATHER_API_KEY
    use_mock = Config.USE_MOCK_WEATHER

    normalized_city = city_name.strip().lower()
    fallback_summary = MOCK_WEATHER.get(normalized_city, "Clear")
    
    if use_mock:
        return {
            **DEFAULT_WEATHER_DATA, 
            "ok": True,
            "summary": fallback_summary,
            "description": fallback_summary,
            "error": None
        }

    if not api_key:
        return {
            **DEFAULT_WEATHER_DATA, 
            "ok": True,
            "description": fallback_summary,  # overrides
            "error": "missing_api_key" # overrides
        }

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial" # imperial for F and metric for celsius

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return{
            "ok": True,
            "summary": data['weather'][0]['main'],
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description'], 
            "error": None      
        }  
    except (KeyError, TypeError):
        logger.error(f"Unexpected data format from weather API for {city_name}")
        return {**DEFAULT_WEATHER_DATA, "summary":fallback_summary, "error": "parse_error"}
    except requests.exceptions.Timeout:
        return {**DEFAULT_WEATHER_DATA, "summary":fallback_summary, "error": "timeout"}
    except requests.exceptions.RequestException:
        return {**DEFAULT_WEATHER_DATA, "summary":fallback_summary, "error": "network_error"}