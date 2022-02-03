# helper functions for views
import requests
import os

from dotenv import load_dotenv
load_dotenv()

my_api_key = os.getenv("openweather_api_key")
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

def get_cities_weather(cities, dic=False):
    weather_data = []
    if dic:
        weather_data = {}
        
    for city in cities:
        r = requests.get(url.format(city.name, my_api_key)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        if dic:
            weather_data[city.name] = city_weather
        else:
            weather_data.append(city_weather)

    return weather_data