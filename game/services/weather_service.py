import os
import requests

from game.config import Config

DEFAULT_WEATHER_DATA = {
    "ok": False,
    "summary": "clear",
    "temperature": 30,
    "description": "clear sky",
    "error": "unavailable"
}
def get_weather_by_city(city_name):
    api_key = Config.OPENWEATHER_API_KEY
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial" # imperial for F and metric for celsius
        if not api_key:
            return {**DEFAULT_WEATHER_DATA}
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return{
                "ok": True,
                "summary": data['weather'][0]['main'],
                "temperature": data['main']['temp'],
                "description": data['weather'][0]['description'], 
                "error": None      
            }

        else:
            print("Failed to get weather data")
            return {"summary": "clear", "temperature": 30, "description": "clear sky"} # default values if the API call fails
    except requests.exceptions.Timeout:
        return {**DEFAULT_WEATHER_DATA, "error": "timeout"}
    except requests.exceptions.HTTPError:
        return {**DEFAULT_WEATHER_DATA, "error": "http_error"}
    except requests.exceptions.RequestException:
        return {**DEFAULT_WEATHER_DATA, "error": "network_error"}