import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests
from geopy.distance import geodesic





# Load your Google Maps API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def calculate_price(departure,destination):
    distance = geodesic(get_geocode(departure), get_geocode(destination)).km
    base_fare = 5.0  # Base fare in dollars
    per_km_rate = 1.5  # Rate per kilometer
    price = base_fare + (distance * per_km_rate)
    return round(price, 2)

def get_geocode(address):
    # API endpoint for geocoding
    geocode_endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'

    # Parameters for the API request
    params = {
        'address': address,
        'key': API_KEY  
    }

    # Send a GET request to the Geocoding API
    response = requests.get(geocode_endpoint, params=params)

    # Parse the JSON response
    data = response.json()

    # Check if the response contains results
    if 'results' in data and len(data['results']) > 0:
        # Extract latitude and longitude from the first result
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        # If no results are found, return None
        return None