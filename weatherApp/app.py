""" Weather app main module
This module initializes and runs the Flask web application
for fetching and displaying weather forecasts based on user input.
It defines routes for the home page and the search functionality."""
import json

from flask import Flask, render_template, request, redirect, Response
import api_requests


weather_app = Flask(__name__)

@weather_app.route('/', methods=['GET'])
def home_page():
    """Renders home page. Returns rendered template of home page"""
    return render_template('home.html')

@weather_app.route('/search', methods=['GET'])
def process_data():
    """Handle weather search requests from the user.
    Retrieves the location entered by the user, fetches weather data
    using the `api_requests` module, and renders a forecast page
    or an error page depending on the result"""

    user_input = request.args.get('location').strip()

    location, data = api_requests.secure_weather_info(user_input)
    if not location['success']:
        return render_template('error.html', message=location['error'])

    return render_template('forecast.html', location=location, data=data)

if __name__ == '__main__':
    weather_app.run(debug=True)
