import os 
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from config.models import db

class DriverRepository:
    def __init__(self):
        self.ride_orders_ref = db.collection('ride_orders')

    def get_pending_rides(self):
        query = self.ride_orders_ref.where('status', '==', 'pending').stream()
        rides = []
        for doc in query:
            ride = doc.to_dict()
            ride['id'] = doc.id
            rides.append(ride)
        return rides

    def get_ride_order(self, ride_id):
        ride_order_ref = self.ride_orders_ref.document(str(ride_id))
        ride_order = ride_order_ref.get()
        if ride_order.exists:
            return ride_order.to_dict()
        return None

    def update_ride_order(self, ride_id, update_data):
        ride_order_ref = self.ride_orders_ref.document(str(ride_id))
        ride_order_ref.update(update_data)