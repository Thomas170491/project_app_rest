from config.models import RideOrder

class UsersMapper:

    @staticmethod
    def map_to_order_ride(data, user_id, price):
        return RideOrder(
            name=data['name'],
            departure=data['departure'],
            destination=data['destination'],
            time=data['time'],
            user_id=user_id,
            price=price
        )

    @staticmethod
    def map_to_order_confirmation(ride_order):
        return {
            'ride_id': ride_order.id,
            'name': ride_order.user.name,
            'departure': ride_order.departure,
            'destination': ride_order.destination,
            'time': ride_order.time
        }

    @staticmethod
    def map_to_order_status(rides):
        return [{'ride_id': ride.id, 'status': ride.status} for ride in rides]
