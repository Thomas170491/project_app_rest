import os
import sys
import requests
import googlemaps

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from user_routes.user_repository import UsersRepository
from user_routes.user_mapper import UsersMapper
from flask import url_for
from flask_login import login_user
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash

from marshmallow import ValidationError
from user_routes.dto.requests.user_request import (
    LoginRequestDTO, OrderRideRequestDTO, CalculatePriceRequestDTO, 
    CreatePaymentRequestDTO, ExecutePaymentRequestDTO
)
from user_routes.dto.responses.user_response import (
    LoginResponseDTO, OrderRideResponseDTO, OrderConfirmationResponseDTO, 
    OrderStatusResponseDTO, CalculatePriceResponseDTO, PayResponseDTO, 
    CreatePaymentResponseDTO, ExecutePaymentResponseDTO
)
from config.models import load_user,db

# Load your Google Maps API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=API_KEY)

user_repository = UsersRepository()

class UsersService:
    def __init__(self):
        self.user_repository = UsersRepository()
        self.user_mapper = UsersMapper()

    def calculate_distance(self, departure, destination):
        try:
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

    def calculate_price(self, departure, destination):
        try:
            distance = self.calculate_distance(departure, destination)
            if distance is not None:
                base_fare = 5.0
                per_km_rate = 1.5
                price = base_fare + (distance * per_km_rate)
                return round(price, 2)
            else:
                return None
        except ValueError as e:
            print("Error calculating price:", e)
            return None

    def get_paypal_access_token(self):
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

    def login(self, data):
        try:
            validated_data = LoginRequestDTO().load(data)
            print(validated_data)
        except ValidationError as err:
            return {'error': err.messages}

        username = validated_data['username']
        password = validated_data['password']

        # Retrieve user from repository or Firestore based on username
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return {'error': 'Invalid username or password'}

        # Check if the password matches using Flask's password hash checker
        if not check_password_hash(user['password_hash'], password):
            return {'error': 'Invalid username or password'}

        # Login the user using Flask-Login's login_user function
        user_ref = user_repository.get_user_id_by_username(username)
        user_load = load_user(user_ref)  # Use load_user callback to load user into sessionuse
        login_user(user_load, remember=validated_data.get('remember_me', False))

        # Determine next_page after login
        next_page = validated_data.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for(f'{user["role"]}s.dashboard')

        # Prepare response data
        response_data = {'message': 'Login successful', 'next_page': next_page} 
        
        return LoginResponseDTO().dump(response_data)
    
    def order_ride(self, data, user_id):
        try:
            validated_data = OrderRideRequestDTO().load(data)
            
        except ValidationError as err:
            return {'error': err.messages}

        price = self.calculate_price(validated_data['departure'], validated_data['destination'])
        if not isinstance(price, (int, float)):
            return {'error': 'Calculated price is not a valid number'}

        order_data = self.user_mapper.map_to_order_ride(validated_data, user_id, price)
        print(order_data)
        self.user_repository.add_order(order_data)
        
        response_data = {
            'message': 'Your ride is on the way',
            'ride_id': order_data.id,
            'price': price
        }
        return OrderRideResponseDTO().dump(response_data)

    def order_confirmation(self, ride_id, user_id):
        ride_order = self.user_repository.get_ride_order(ride_id)
        if ride_order['user_id'] != user_id:
           
            return {'error': 'Forbidden'}
        
        response_data = self.user_mapper.map_to_order_confirmation(ride_order)
        return OrderConfirmationResponseDTO().dump(response_data)


    def calculate_price_service(self, data):
        try:
            validated_data = CalculatePriceRequestDTO().load(data)
        except ValidationError as err:
            return {'error': err.messages}

        price = self.calculate_price(validated_data['departure'], validated_data['destination'])
        response_data = {'price': price}
        return CalculatePriceResponseDTO().dump(response_data)

    def order_status_detail(self, ride_id, user_id):
        ride_order = self.user_repository.get_ride_order(ride_id)
        if ride_order is None or ride_order['user_id'] != user_id:
            return {'error': 'Not found'}
        
        return {'ride_status': ride_order['status']}

    def pay(self, ride_id, user_id):
        ride_order = self.user_repository.get_ride_order(ride_id)
        if ride_order['user_id'] != user_id:
            return {'error': 'Forbidden'}
        
        response_data = {
            'ride_id': ride_id,
            'name': ride_order['name'],
            'departure': ride_order['departure'],
            'destination': ride_order['destination'],
            'time': ride_order['time'],
            'client_id': os.getenv('PAYPAL_CLIENT_ID')
        }
        return PayResponseDTO().dump(response_data)

    def create_payment(self, ride_id, form_data):
        try:
            validated_data = CreatePaymentRequestDTO().load(form_data)
        except ValidationError as err:
            return {'error': err.messages}

        access_token = self.get_paypal_access_token()
        total_amount = self.calculate_price(validated_data['departure'], validated_data['destination'])

        payment_data = {
            "intent": "sale",
            "redirect_urls": {
                "return_url": url_for('users.execute_payment', ride_id=ride_id, _external=True),
                "cancel_url": url_for('users.pay', ride_id=ride_id, _external=True),
            },
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(total_amount),
                    "currency": "USD"
                },
                "description": "Ride Payment"
            }]
        }

        response = requests.post(
            f"{os.getenv('PAYPAL_API_BASE')}/v1/payments/payment",
            json=payment_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
        )

        if response.status_code == 201:
            payment = response.json()
            for link in payment['links']:
                if link['rel'] == 'approval_url':
                    response_data = {'approval_url': link['href']}
                    return CreatePaymentResponseDTO().dump(response_data)
            return {'error': 'No approval_url found in PayPal response'}
        else:
            return {'error': f'Error creating payment: {response.status_code}'}
    def execute_payment(self, ride_id, args):
        try:
            validated_data = ExecutePaymentRequestDTO().load(args)
        except ValidationError as err:
            return {'error': err.messages}

        access_token = self.get_paypal_access_token()

        response = requests.post(
            f"{os.getenv('PAYPAL_API_BASE')}/v1/payments/payment/{validated_data['paymentId']}/execute",
            json={"payer_id": validated_data['PayerID']},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
        )

        payment = response.json()
        try:
            if payment['state'] == 'approved':
                response_data = {'message': 'Payment successful'}
                return ExecutePaymentResponseDTO().dump(response_data)
            else:
                response_data = {'error': 'Payment failed. Please try again.'}
                return response_data
        except KeyError:
            # Handle the case where 'state' key is not found in payment response
            return {'error': 'Unexpected response from PayPal API'}
