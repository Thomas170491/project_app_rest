import os

import requests



def verify_address(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': os.getenv('GOOGLE_MAPS_API_KEY')
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        return True, data['results'][0]['formatted_address']
    else:
        return False, None