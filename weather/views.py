from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from django.http import JsonResponse
from .functions import get_cities_weather

import requests
import os

from dotenv import load_dotenv
load_dotenv()

my_api_key = os.getenv("openweather_api_key")

# Create your views here.


def is_ajax(request):
	return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

	cities = City.objects.filter(user = request.user)

	err_msg = ''
	message = ''
	message_class = ''

	if is_ajax(request=request):
		weather_data = get_cities_weather(cities, dic=True)
		return JsonResponse({'weather_update': weather_data}, status=200)

	if request.method == 'POST':
		form = CityForm(request.POST)

		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city_count = City.objects.filter(user = request.user, name=new_city).count()	

			if existing_city_count == 0:
				r = requests.get(url.format(new_city, my_api_key)).json()
				if r['cod'] == 200:
					obj = form.save(commit = False)
					obj.user = request.user
					obj.save()
				else:
					err_msg = 'City does not exist in the world!'
			else:
				err_msg = 'City already exists in the database!'

		# print(form.errors)

		if err_msg:
			message = err_msg
			message_class = 'is-danger'
		else:
			message = 'City added successfully!'
			message_class = 'is-success'

	form = CityForm()
	
	weather_data = get_cities_weather(cities)
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

