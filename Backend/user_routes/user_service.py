import os
import sys
import requests
import googlemaps
from flask import url_for
from flask_login import login_user
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from user_routes.user_repository import UsersRepository
from user_routes.user_mapper import UsersMapper
from user_routes.dto.requests.user_request import (
    LoginRequestDTO, OrderRideRequestDTO, CalculatePriceRequestDTO, 
    CreatePaymentRequestDTO, ExecutePaymentRequestDTO
)
from user_routes.dto.responses.user_response import (
    LoginResponseDTO, OrderRideResponseDTO, OrderConfirmationResponseDTO, 
    OrderStatusResponseDTO, CalculatePriceResponseDTO, PayResponseDTO, 
    CreatePaymentResponseDTO, ExecutePaymentResponseDTO
)
from config.models import load_user, db

# Load your Google Maps API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

if not API_KEY:
    raise ValueError("Google Maps API key is not set in environment variables.")

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=API_KEY)

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
        try:
            response = requests.post(
                f"{os.getenv('PAYPAL_API_BASE')}/v1/oauth2/token",
                headers={
                    "Accept": "application/json",
                    "Accept-Language": "en_US",
                },
                auth=(os.getenv('PAYPAL_CLIENT_ID'), os.getenv('PAYPAL_CLIENT_SECRET')),
                data={"grant_type": "client_credentials"}
            )
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.RequestException as e:
            print("Error getting PayPal access token:", e)
            return None

    def login(self, data):
        try:
            validated_data = LoginRequestDTO().load(data)
        except ValidationError as err:
            return {'error': err.messages}

        username = validated_data['username']
        password = validated_data['password']

        user = self.user_repository.get_user_by_username(username)
        if not user:
            return {'error': 'Invalid username or password'}

        if not check_password_hash(user['password_hash'], password):
            return {'error': 'Invalid username or password'}

        user_ref = self.user_repository.get_user_id_by_username(username)
        user_load = load_user(user_ref)
        login_user(user_load, remember=validated_data.get('remember_me', False))
        
        access_token = create_access_token(identity=user['username'])

        next_page = validated_data.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for(f'{user["role"]}s.dashboard')

        response_data = {'message': 'Login successful', 'next_page': next_page, 'status': 200, 'acces_token' : access_token}
        return LoginResponseDTO().dump(response_data)

    def order_ride(self, data, user_id):
        try:
            validated_data = OrderRideRequestDTO().load(data)
        except ValidationError as err:
            return {'error': err.messages}

        price = self.calculate_price(validated_data['departure'], validated_data['destination'])
        if price is None:
            return {'error': 'Calculated price is not valid'}

        order_data = self.user_mapper.map_to_order_ride(validated_data, user_id, price)
        self.user_repository.add_order(order_data)

        response_data = {
            'message': 'Your ride is on the way',
            'ride_id': order_data.id,
            'price': price
        }
        return OrderRideResponseDTO().dump(response_data)

    def order_confirmation(self, ride_id, user_id):
        ride_order = self.user_repository.get_ride_order(ride_id)
        if ride_order is None or ride_order['user_id'] != user_id:
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
        if ride_order is None or ride_order['user_id'] != user_id:
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
        if not access_token:
            return {'error': 'Could not retrieve PayPal access token'}

        total_amount = self.calculate_price(validated_data['departure'], validated_data['destination'])
        if total_amount is None:
            return {'error': 'Invalid total amount'}

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

        try:
            response = requests.post(
                f"{os.getenv('PAYPAL_API_BASE')}/v1/payments/payment",
                json=payment_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                }
            )
            response.raise_for_status()

            payment = response.json()
            approval_url = next((link['href'] for link in payment.get('links', []) if link['rel'] == 'approval_url'), None)

            if approval_url:
                response_data = {'approval_url': approval_url}
                return CreatePaymentResponseDTO().dump(response_data)
            else:
                return {'error': 'No approval_url found in PayPal response'}
        except requests.RequestException as e:
            print("Error creating payment:", e)
            return {'error': f'Error creating payment: {e}'}

    def execute_payment(self, ride_id, args):
        try:
            validated_data = ExecutePaymentRequestDTO().load(args)
        except ValidationError as err:
            return {'error': err.messages}

        access_token = self.get_paypal_access_token()
        if not access_token:
            return {'error': 'Could not retrieve PayPal access token'}

        try:
            response = requests.post(
                f"{os.getenv('PAYPAL_API_BASE')}/v1/payments/payment/{validated_data['paymentId']}/execute",
                json={"payer_id": validated_data['PayerID']},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                }
            )
            response.raise_for_status()
            
            payment = response.json()
            if payment.get('state') == 'approved':
                response_data = {'message': 'Payment successful'}
                return ExecutePaymentResponseDTO().dump(response_data)
            else:
                return {'error': 'Payment failed. Please try again.'}
        except requests.RequestException as e:
            print("Error executing payment:", e)
            return {'error': 'Unexpected error occurred during payment execution'}
