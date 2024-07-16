class DriverMapper:
    def map_to_display_rides(self, rides):
        return [{'ride_id': ride['id'], 'status': ride['status'], 'departure': ride['departure'], 'destination': ride['destination']} for ride in rides]

    def map_to_accept_ride(self, ride_order):
        return {
            'ride_id': ride_order['id'],
            'status': ride_order['status'],
            'driver_id': ride_order['driver_id'],
            'accepted_time': ride_order['accepted_time']
        }

    def map_to_decline_ride(self, ride_order):
        return {
            'ride_id': ride_order['id'],
            'status': ride_order['status'],
            'driver_id': ride_order['driver_id']
        }