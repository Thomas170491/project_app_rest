import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim




# Load your Google Maps API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def get_geocode(address):
    geolocator = Nominatim(user_agent="ride_order_app")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError("Could not geocode address: {}".format(address))

def calculate_price(departure,destination):
    try:
        departure_coords = get_geocode(departure)
        destination_coords = get_geocode(destination)
        distance = geodesic(departure_coords, destination_coords).km
        base_fare = 5.0  # Base fare in dollars
        per_km_rate = 1.5  # Rate per kilometer
        price = base_fare + (distance * per_km_rate)
        return round(price, 2)
    except ValueError as e:
        print(e)
        return None

def get_paypal_access_token():
    response = requests.post(
        f"{os.getenv('PAYPAL_API_BASE')}/v1/oauth2/token",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        auth=(os.getenv('PAYPAL_CLIENT_ID'), os.getenv('PAYPAL_CLIENT_SECRET')),
        data={"grant_type": "client_credentials"}
    )
    return response.json()['access_token']

# Example usage
departure_address = 'Rue Caroline 34 1227 Les Acacias'
destination_address = 'Rue Muzy 13 1207 Genève'
price = calculate_price(departure_address, destination_address)
print(f"The calculated price is ${price}")