import os
import requests

from game.config import Config

def get_weather_by_city(city_name):
    api_key = Config.OPENWEATHER_API_KEY
    try:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial" # imperial for F and metric for celsius
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return{
                "summary": data['weather'][0]['main'],
                "temperature": data['main']['temp'],
                "description": data['weather'][0]['description'],       
            }
        else:
            print("Failed to get weather data")
            return {"summary": "clear", "temperature": 30, "description": "clear sky"} # default values if the API call fails
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return {"summary": "clear", "temperature": 30, "description": "clear sky"} # default values if the API call fails

