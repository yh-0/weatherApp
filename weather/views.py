import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid=6a81c9fabf82d1d0ea5eb40ebcafa130'
    unit = request.POST.get('unit_select', 'metric')

    units_list = {
        'metric' : '°C',
        'imperial' : '°F',
        'standard' : 'K'
    }

    if request.method == 'POST' and request.POST.get('name'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city, unit)).json()

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
        'units_list' : units_list,
        'units' : units_list.get(unit)
    }
    return render(request, 'weather/weather.html', context)