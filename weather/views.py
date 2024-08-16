# views.py

from django.shortcuts import render
from django.conf import settings
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    api_key = settings.OPENWEATHERMAP_API_KEY

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)  # Print form errors for debugging

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        try:
            response = requests.get(url.format(city.name, api_key))
            response.raise_for_status()  # Raises an HTTPError for bad responses
            city_weather = response.json()
            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
            weather_data.append(weather)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data for {city.name}: {e}")

    context = {
        'form': form,
        'weather_data': weather_data
    }
    return render(request, 'weather/index.html', context)