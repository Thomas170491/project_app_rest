import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from config.models import RideOrder
from user_routes.user_repository import UsersRepository

user_repository = UsersRepository()

class UsersMapper:
    
    def map_to_order_ride(self, data, user_id, price):
        return RideOrder(
            id = user_id,
            name=data['name'],
            departure=data['departure'],
            destination=data['destination'],
            time=data['time'],
            user_id=user_id,
            price=price
        )
        

    def map_to_order_confirmation(self, ride_order):
        return {
            'ride_id': ride_order['id'],
            'name': ride_order['name'],
            'departure': ride_order['departure'],
            'destination': ride_order['destination'],
            'time': ride_order['time']
        }

    def map_to_order_status(self, rides):
        return [{'ride_id': ride.id, 'status': ride.status} for ride in rides]

