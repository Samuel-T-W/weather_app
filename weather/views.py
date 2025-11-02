from typing import Optional
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import requests
import sentry_sdk
import logging

import os

from dotenv import load_dotenv
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
logger = logging.getLogger(__name__)

# Create your views here.

def get_city_coordinates(city_name) -> list:
	""" Convert city names into longitude and lattiude values using OpenWeatherMap API"""
	#TODO: add state and country code as some cities share same names
	geocode_url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}"

	try:
		response = requests.get(geocode_url.format(city_name, OPENWEATHER_API_KEY)).json()
		# breakpoint()
		#TODO: handle city name not found more gracefuly (let the user now instead of generic message)
		print(f"response:{response}")
		return response[0]['lat'], response[0]['lon']
	except Exception as e:
		logger.error(f"unexpected error occured for city: {city_name} with: {e}")
		sentry_sdk.capture_exception(e)
		return []

def index(request):
	url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&units=metric&appid={}'

	err_msg = ''
	message = ''
	message_class = ''

	if request.method == 'POST':
		form = CityForm(request.POST)

		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city_count = City.objects.filter(user = request.user, name=new_city).count()	

			if existing_city_count == 0:
				#TODO handle no lat, long response more gracefully 
				lat, long = get_city_coordinates(new_city)
				r = requests.get(url.format(lat, long, OPENWEATHER_API_KEY)).json()
				if "current" in r:
					obj = form.save(commit = False)
					obj.user = request.user
					obj.save()
				else:
					err_msg = 'City does not exist in the world!'
			else:
				err_msg = 'City already exists in you list of cities!'

		if err_msg:
			message = err_msg
			message_class = 'is-danger'
		else:
			message = 'City added successfully!'
			message_class = 'is-success'

	form = CityForm()

	cities = City.objects.filter(user = request.user)

	weather_data = []
	context={}
	
	for city in cities:
		try:
			lat, long = get_city_coordinates(city.name)
			r = requests.get(url.format(lat, long, OPENWEATHER_API_KEY)).json()
			# breakpoint()
			print(f"city:{city} r:{r}")

			if "cod" in r:
				sentry_sdk.capture_message(
					f"Weather API error {r['cod']}: {r['message']}",
					level="error"
				)
				continue

			city_weather = {
				'city' : city.name,
				'temperature' : r['current']['temp'],
				'description' : r['current']['weather'][0]['description'],
				'icon' : r['current']['weather'][0]['icon'],
			}

			weather_data.append(city_weather)
   
		except Exception as e:
			logger.error(f"unexpected error occured for city: {city.name} with: {e}")
			sentry_sdk.capture_exception(e)

	context = {
		'weather_data' : weather_data, 
		'form' : form,
		'message' : message,
		'message_class' : message_class
	}

	return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
	City.objects.get(user = request.user, name=city_name).delete()
	
	return redirect('home')