import requests
import logging

from game.config import Config

logger = logging.getLogger(__name__)

DEFAULT_WEATHER_DATA = {
    "ok": False,
    "summary": "clear",
    "temperature": 30,
    "description": "clear sky",
    "error": "unavailable"
}

def get_weather_by_city(city_name):
    api_key = Config.OPENWEATHER_API_KEY
    if not api_key:
        return {**DEFAULT_WEATHER_DATA}
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial" # imperial for F and metric for celsius

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            logger.warning(f"Failed to get weather data for {city_name}: {response.status_code}")
            return {**DEFAULT_WEATHER_DATA, "error": f"HTTP {response.status_code}"}
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
        return {**DEFAULT_WEATHER_DATA, "error": "parse_error"}
    except requests.exceptions.Timeout:
        return {**DEFAULT_WEATHER_DATA, "error": "timeout"}
    except requests.exceptions.RequestException:
        return {**DEFAULT_WEATHER_DATA, "error": "network_error"}