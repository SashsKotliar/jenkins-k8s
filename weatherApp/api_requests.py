"""Weather API request utilities.

This module provides functions for interacting with the Open-Meteo API.
It includes geocoding lookups, weather data retrieval, and error-handled
API access for use in the main Flask application.
"""
import requests

def request_to_api(url, params):
    """Sends request to api and returns a response as json"""
    response = requests.get(url, params, timeout=10)  # timeout error
    response.raise_for_status()
    return response.json()


def location_data(location):
    """Makes API call to get lat and lon of user asked location
    Returns dictionary with needed data"""
    params = {
        'name': location,
        'count': 1
    }
    resp_json = request_to_api(
        'https://geocoding-api.open-meteo.com/v1/search', params
    )  # httpError
    result = resp_json['results'][0]  # key error
    return {
        'name': result['name'],
        'lat': result['latitude'],
        'lon': result['longitude'],
        'country': result['country']
    }


def get_weather_info(location):
    """Gets user asked location and returns dictionary with weather data """
    loc_info = location_data(location)
    params = {
        'latitude': loc_info['lat'],
        'longitude': loc_info['lon'],
        'daily': 'temperature_2m_min,temperature_2m_max,relative_humidity_2m_mean'
    }
    weather_response = request_to_api(
        'https://api.open-meteo.com/v1/forecast', params
    )
    week = weather_response['daily']
    days = week['time']
    night_temp = week['temperature_2m_min']
    day_temp = week['temperature_2m_max']
    humidity = week['relative_humidity_2m_mean']
    forecast = []
    for day in range(len(days)):
        forecast.append({
            'date': days[day],
            'day_temp': int(day_temp[day]),
            'night_temp': int(night_temp[day]),
            'humidity': humidity[day]
        })
    if loc_info['country'] == loc_info['name']:
        return {'success': True, 'country': loc_info['country']}, forecast
    return ({
        'success': True,
        'country': loc_info['country'],
        'city': loc_info['name']
            }, forecast)


def secure_weather_info(location):
    """Error handling.
    Returns dictionary with weather data if no exception was found
    Returns dictionary with exception definition if it was found"""
    try:
        return get_weather_info(location)
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Connection Error!'}, []
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Timeout Error!'}, []
    except requests.exceptions.HTTPError:
        return {'success': False, 'error': 'Http Error!'}, []
    except KeyError:
        return {'success': False, 'error': 'Error! Invalid location!'}, []
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected Error: {type(e).__name__}'
        }, []



