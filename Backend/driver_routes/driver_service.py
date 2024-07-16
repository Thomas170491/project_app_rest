import os
import requests
from datetime import datetime
from repositories.driver_repository import DriverRepository
from mappers.driver_mapper import DriverMapper

class DriverService:
    def __init__(self):
        self.driver_repository = DriverRepository()
        self.driver_mapper = DriverMapper()

    def verify_address(self, address):
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

    def get_dashboard(self):
        return {'message': 'Welcome to the driver dashboard'}

    def display_rides(self):
        rides = self.driver_repository.get_pending_rides()
        return self.driver_mapper.map_to_display_rides(rides)

    def accept_ride(self, ride_id, driver_id):
        ride_order = self.driver_repository.get_ride_order(ride_id)
        if ride_order['status'] != 'pending':
            return {'error': 'Ride has already been accepted or completed'}
        
        # Verify the departure and destination addresses
        departure_verified, formatted_departure = self.verify_address(ride_order['departure'])
        destination_verified, formatted_destination = self.verify_address(ride_order['destination'])

        if not departure_verified or not destination_verified:
            return {'error': 'Invalid departure or destination address'}
        
        update_data = {
            'driver_id': driver_id,
            'status': 'accepted',
            'accepted_time': datetime.utcnow(),
            'departure': formatted_departure,
            'destination': formatted_destination
        }
        self.driver_repository.update_ride_order(ride_id, update_data)
        ride_order.update(update_data)
        return self.driver_mapper.map_to_accept_ride(ride_order)

    def decline_ride(self, ride_id, driver_id):
        ride_order = self.driver_repository.get_ride_order(ride_id)
        if ride_order['status'] != 'pending':
            return {'error': 'Ride has already been accepted or completed'}
        
        # Verify the departure and destination addresses
        departure_verified, formatted_departure = self.verify_address(ride_order['departure'])
        destination_verified, formatted_destination = self.verify_address(ride_order['destination'])

        if not departure_verified or not destination_verified:
            return {'error': 'Invalid departure or destination address'}
        
        update_data = {
            'driver_id': driver_id,
            'status': 'declined',
            'departure': formatted_departure,
            'destination': formatted_destination
        }
        self.driver_repository.update_ride_order(ride_id, update_data)
        ride_order.update(update_data)
        return self.driver_mapper.map_to_decline_ride(ride_order)
