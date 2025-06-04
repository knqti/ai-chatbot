from geopy.geocoders import Nominatim
import json
import requests

def get_coordinates(location: str):
    print('Getting coordinates')
    geolocator = Nominatim(user_agent='ai-chatbot', timeout=10)
    location = geolocator.geocode(location)
    return location.latitude, location.longitude

def get_forecast_url(latitude, longitude):
    print('Getting forecast url')
    end_point = f'https://api.weather.gov/points/{latitude},{longitude}'
    results = requests.get(end_point)
    data = json.loads(results.text)
    return data['properties']['forecast']

def get_forecast_weather(forecast_url):
    print('Getting the forecast')
    results = requests.get(forecast_url)
    data = json.loads(results.text)
    day_weather = data['properties']['periods'][0]['detailedForecast']
    night_weather = data['properties']['periods'][1]['detailedForecast']
    return day_weather, night_weather

def get_weather(address_location: str) -> tuple[str, str]:
    '''Get daytime and nighttime weather based off location.
    
    Args:
        address_location: General address/location match (ie, Pasadena CA)

    Returns:
        Tuple of (daytime weather, nighttime weather)
    '''
    latitude, longitude = get_coordinates(address_location)
    url = get_forecast_url(latitude, longitude)
    return get_forecast_weather(url)

