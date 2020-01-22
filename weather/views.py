from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
#from .api import your_api_key
import requests

import os

from dotenv import load_dotenv
load_dotenv()

my_api_key = os.getenv("my_api_key")

# Create your views here.

def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'


	err_msg = ''
	message = ''
	message_class = ''

	if request.method == 'POST':
		form = CityForm(request.POST)

		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city_count = City.objects.filter(name=new_city).count()
			
			if existing_city_count == 0:
				r = requests.get(url.format(new_city, my_api_key)).json()

				if r['cod'] == 200:
					form.save()
				else:
					err_msg = 'City does not exist in the world!'
			else:
				err_msg = 'City already exists in the database!'

		if err_msg:
			message = err_msg
			message_class = 'is-danger'
		else:
			message = 'City added successfully!'
			message_class = 'is-success'

	form = CityForm()

	cities = City.objects.all()

	weather_data = []

	for city in cities:

		r = requests.get(url.format(city, my_api_key)).json()

		city_weather = {
			'city' : city.name,
			'temperature' : r['main']['temp'],
			'description' : r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
		}

		weather_data.append(city_weather)

	context = {
		'weather_data' : weather_data, 
		'form' : form,
		'message' : message,
		'message_class' : message_class
	}

	return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
	City.objects.get(name=city_name).delete()
	
	return redirect('home')