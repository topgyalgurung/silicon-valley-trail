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
            temperature = data['main']['temp']
            description = data['weather'][0]['description']

            print(f"Temperature: {temperature} kelvin, Description: {description}")
            return data
        else:
            print("Failed to get weather data")
            return None
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return None

