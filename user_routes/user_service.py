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
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        status = data.get('status')
        if status == 'OK':
            rows = data.get('rows')
            if rows:
                elements = rows[0].get('elements')
                if elements:
                    element = elements[0]
                    if element.get('status') == 'OK':
                        distance_in_meters = element['distance']['value']
                        distance_in_km = distance_in_meters / 1000
                        return distance_in_km
    except requests.exceptions.RequestException as e:
        print(f"Error fetching distance: {e}")
    return None

def calculate_price(departure, destination):
    distance = get_distance(departure, destination)
    print(distance)
    if distance is not None:
        base_fare = 5.0  # Base fare in dollars
        per_km_rate = 1.5  # Rate per kilometer
        price = base_fare + (distance * per_km_rate)
        return price
    return 0.0



