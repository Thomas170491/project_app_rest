import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from Backend.config.models import db
from werkzeug.security import generate_password_hash, check_password_hash


class UsersRepository:
    def __init__(self):
        self.collection = db.collection('users')

    def get_user_by_username(self, username):
        query = self.collection.where('username', '==', username).limit(1).stream()
        users = [user.to_dict() for user in query]
        if users:
            return users[0]
        return None
    
    def get_user_id_by_username(self,username):
        # Reference to the 'users' collection
        users_ref = db.collection('users')

        # Query users collection by username
        query = users_ref.where('username', '==', username).limit(1)

        # Retrieve documents that match the query
        docs = query.get()

        # Iterate through the documents (there should be only one matching document)
        for doc in docs:
            return doc.id  # Return the document ID

        # Return None if no matching document found
        return None


    def add_user(self, user_data):
        h_pwd = generate_password_hash(user_data['password'])
        user_data['password_hash'] = h_pwd
        self.collection.add(user_data)

    def check_password(self, stored_hash, password):
        return check_password_hash(stored_hash, password)
    
    def add_order(self, order_data):
        """
        Add a ride order to the 'ride_orders' collection.
        
        Parameters:
        - user_id (str): The ID of the user placing the order.
        - order_data (dict): The data of the order being placed.
        
        Returns:
        - dict: Result of the operation, containing success or error message.
        """
        
        try:
            self.collection.add(order_data)
            return {'message': 'Order added successfully'}
        except Exception as e:
            return {'error': str(e)}
        
    def get_ride_orders_by_user(self, user_id):
        ride_ref = db.collection('ride_orders')
        query = ride_ref.where('user_id', '==', user_id).limit(1)
        docs = query.get()
        for doc in docs:
            return doc.to_dict()
        return None
     
    def get_ride_order(self,ride_id):
        ride_ref = db.collection('ride_orders')
        print(ride_ref)
        query = ride_ref.where('ride_id', '==', ride_id).limit(1)
        docs = query.get()
        for doc in docs:
            return doc.to_dict()
        return None
        
   
     
