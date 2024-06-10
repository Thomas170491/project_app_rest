import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import googlemaps




# Load your Google Maps API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=API_KEY)

def calculate_distance(departure, destination):
    try:
        # Make a Distance Matrix request to calculate distance
        matrix = gmaps.distance_matrix(departure, destination, mode='driving', units='metric')
        if matrix['status'] == 'OK':
            distance_in_meters = matrix['rows'][0]['elements'][0]['distance']['value']
            distance_in_kilometers = distance_in_meters / 1000
            return distance_in_kilometers
        else:
            print("Error: Distance calculation failed - ", matrix['status'])
            return None
    except Exception as e:
        print("Error calculating distance:", e)
        return None

def calculate_price(departure, destination):
    try:
        distance = calculate_distance(departure, destination)
        if distance is not None:
            base_fare = 5.0  # Base fare in dollars
            per_km_rate = 1.5  # Rate per kilometer
            price = base_fare + (distance * per_km_rate)
            return round(price, 2)
        else:
            return None
    except ValueError as e:
        print("Error calculating price:", e)
        return None

def get_paypal_access_token():
    response = requests.post(
        f"{os.getenv('PAYPAL_API_BASE')}/v1/oauth2/token",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        auth=(os.getenv('PAYPAL_CLIENT_ID'), os.g('PAYPAL_CLIENT_SECRET')),
        data={"grant_type": "client_credentials"}
    )
    return response.json()['access_token']

# Example usage
departure_address = 'Rue Caroline 34 1227 Les Acacias'
destination_address = 'Rue Muzy 13 1207 Genève'
price = calculate_price(departure_address, destination_address)
print(f"The calculated price is ${price}")