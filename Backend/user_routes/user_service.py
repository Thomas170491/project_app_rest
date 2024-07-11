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

# Load your Google Maps API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=API_KEY)

class UsersService:

    @staticmethod
    def calculate_distance(departure, destination):
        try:
            # Make a Distance Matrix request to calculate distance
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

    @staticmethod
    def calculate_price(departure, destination):
        try:
            distance = UsersService.calculate_distance(departure, destination)
            if distance is not None:
                base_fare = 5.0  # Base fare in dollars
                per_km_rate = 1.5  # Rate per kilometer
                price = base_fare + (distance * per_km_rate)
                return round(price, 2)
            else:
                return None
        except ValueError as e:
            print("Error calculating price:", e)
            return None

    @staticmethod
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

    @staticmethod
    def login(data):
        try:
            validated_data = LoginRequestDTO().load(data)
        except ValidationError as err:
            return {'error': err.messages}
        
        user = UsersRepository.get_user_by_username(validated_data['username'])
        if user and user.check_password(validated_data['password']):
            login_user(user, remember=validated_data.get('remember_me', False))
            next_page = validated_data.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for(f'{user.role}s.dashboard')
            response_data = {'message': 'Login successful', 'next_page': next_page}
            return LoginResponseDTO().dump(response_data)
        return {'error': 'Invalid username or password'}
    
    @staticmethod
    def order_ride(data, user_id):
        try:
            validated_data = OrderRideRequestDTO().load(data)
        except ValidationError as err:
            return {'error': err.messages}

        price = UsersService.calculate_price(validated_data['departure'], validated_data['destination'])
        if not isinstance(price, (int, float)):
            return {'error': 'Calculated price is not a valid number'}

        order_data = UsersMapper.map_to_order_ride(validated_data, user_id, price)
        UsersRepository.add_order(order_data)
        response_data = {
            'message': 'Your ride is on the way',
            'ride_id': order_data.id,
            'price': price
        }
        return OrderRideResponseDTO().dump(response_data)
    
    @staticmethod
    def order_confirmation(ride_id, user_id):
        ride_order = UsersRepository.get_ride_order(ride_id)
        if ride_order.user_id != user_id:
            return {'error': 'Forbidden'}
        
        response_data = UsersMapper.map_to_order_confirmation(ride_order)
        return OrderConfirmationResponseDTO().dump(response_data)

    @staticmethod
    def order_status(user_id):
        rides = UsersRepository.get_ride_orders_by_user(user_id)
        response_data = UsersMapper.map_to_order_status(rides)
        return OrderStatusResponseDTO(many=True).dump(response_data)

    @staticmethod
    def calculate_price(data):
        try:
            validated_data = CalculatePriceRequestDTO().load(data)
        except ValidationError as err:
            return {'error': err.messages}

        price = UsersService.calculate_price(validated_data['departure'], validated_data['destination'])
        response_data = {'price': price}
        return CalculatePriceResponseDTO().dump(response_data)

    @staticmethod
    def order_status_detail(ride_id, user_id):
        ride_order = UsersRepository.get_ride_order(ride_id)
        if ride_order is None or ride_order.user_id != user_id:
            return {'error': 'Not found'}
        
        return {'ride_status': ride_order.status}

    @staticmethod
    def pay(ride_id, user_id):
        ride_order = UsersRepository.get_ride_order(ride_id)
        if ride_order.user_id != user_id:
            return {'error': 'Forbidden'}
        
        response_data = {
            'ride_id': ride_id,
            'name': ride_order.name,
            'departure': ride_order.departure,
            'destination': ride_order.destination,
            'time': ride_order.time,
            'client_id': os.getenv('PAYPAL_CLIENT_ID')
        }
        return PayResponseDTO().dump(response_data)

    @staticmethod
    def create_payment(ride_id, form_data):
        try:
            validated_data = CreatePaymentRequestDTO().load(form_data)
        except ValidationError as err:
            return {'error': err.messages}

        access_token = UsersService.get_paypal_access_token()
        total_amount = UsersService.calculate_price(validated_data['departure'], validated_data['destination'])

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

        payment = response.json()
        for link in payment['links']:
            if link['rel'] == 'approval_url':
                response_data = {'approval_url': link['href']}
                return CreatePaymentResponseDTO().dump(response_data)
        return {'error': 'Error creating payment'}

    @staticmethod
    def execute_payment(ride_id, args):
        try:
            validated_data = ExecutePaymentRequestDTO().load(args)
        except ValidationError as err:
            return {'error': err.messages}

        access_token = UsersService.get_paypal_access_token()

        response = requests.post(
            f"{os.getenv('PAYPAL_API_BASE')}/v1/payments/payment/{validated_data['paymentId']}/execute",
            json={"payer_id": validated_data['PayerID']},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
        )

        payment = response.json()
        if payment['state'] == 'approved':
            response_data = {'message': 'Payment successful'}
            return ExecutePaymentResponseDTO().dump(response_data)
        else:
            response_data = {'error': 'Payment failed. Please try again.'}
            return response_data
