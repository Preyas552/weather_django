from django import forms
from .models import City
import requests
from django.conf import settings

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
        api_key = settings.OPENWEATHERMAP_API_KEY

        response = requests.get(url.format(name, api_key))
        if response.status_code != 200:
            raise forms.ValidationError('City not found in OpenWeatherMap API.')
        return name