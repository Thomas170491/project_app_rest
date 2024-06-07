import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests





# Load your Google Maps API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def get_distance(departure, destination):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {
        'origins': departure,
        'destinations': destination,
        'key': API_KEY
    }
    response = requests.get(url, params=params).json()
    
    if response['status'] == 'OK':
        rows = response['rows']
        if rows:
            elements = rows[0]['elements']
            if elements:
                element = elements[0]
                if element['status'] == 'OK':
                    distance_in_meters = element['distance']['value']
                    distance_in_km = distance_in_meters / 1000
                    return distance_in_km
    return None

def calculate_price(departure, destination):
    distance = get_distance(departure, destination)
    if distance is not None:
        base_fare = 5.0  # Base fare in dollars
        per_km_rate = 1.5  # Rate per kilometer
        price = base_fare + (distance * per_km_rate)
        return price
    return 0.0



