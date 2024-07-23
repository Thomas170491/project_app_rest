import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.realpath(__file__))))))

from Backend.utils.decorators import jwt_required_with_role
from flask_smorest import Blueprint
from flask import jsonify, redirect, url_for, request, make_response
from marshmallow.exceptions import ValidationError
from Backend.user_routes.dto.requests.user_request import (
    LoginRequestDTO, OrderRideRequestDTO, CalculatePriceRequestDTO, 
    CreatePaymentRequestDTO, ExecutePaymentRequestDTO
)
from Backend.user_routes.dto.responses.user_response import (
    LoginResponseDTO, OrderRideResponseDTO, OrderConfirmationResponseDTO, 
    OrderStatusResponseDTO, CalculatePriceResponseDTO, PayResponseDTO, 
    CreatePaymentResponseDTO, ExecutePaymentResponseDTO
)
from Backend.user_routes.user_service import UsersService

users = Blueprint("users", "users", url_prefix="/users", description="users routes")

user_service = UsersService()

@users.route("/")
def index():
    return "Hello from users"

@users.route('/login', methods=['GET'])
def login_form():
    return jsonify({"message": "Please submit your login credentials via POST request to this endpoint."})

@users.route('/login', methods=['POST'])
@users.arguments(schema=LoginRequestDTO, location='json')
def user_login(data):
    result, status_code = user_service.login(data)
    return make_response(jsonify(result), status_code)

@users.route('/dashboard', methods=['GET'])
@jwt_required_with_role('user')
def dashboard():
    current_user = request.user
    print(current_user)
    return jsonify({'message': f'Welcome {current_user["username"]}'}), 200

@users.route('/order_ride', methods=['POST'])
@jwt_required_with_role('user')
@users.arguments(schema=OrderRideRequestDTO, location='json')
def order_ride(data):
    result, status_code = user_service.order_ride(data, request.user['id'])
    return make_response(jsonify(result), status_code)

@users.route('/order_confirmation/<ride_id>', methods=['GET'])
@jwt_required_with_role('user')
def order_confirmation(ride_id):
    result, status_code = user_service.order_confirmation(ride_id, request.user['id'])
    return make_response(jsonify(result), status_code)

@users.route('/calculate_price', methods=['POST'])
@jwt_required_with_role('user')
@users.arguments(schema=CalculatePriceRequestDTO, location='json')
def calculate_price(data):
    result, status_code = user_service.calculate_price(data)
    return make_response(jsonify(result), status_code)

@users.route('/order_status/<ride_id>', methods=['GET'])
@jwt_required_with_role('user')
def order_status_detail(ride_id):
    result, status_code = user_service.order_status_detail(ride_id, request.user['id'])
    return make_response(jsonify(result), status_code)

@users.route('/pay/<ride_id>', methods=['GET'])
@jwt_required_with_role('user')
def pay(ride_id):
    result, status_code = user_service.pay(ride_id, request.user['id'])
    return make_response(jsonify(result), status_code)

@users.route('/create_payment/<ride_id>', methods=['POST'])
@jwt_required_with_role('user')
@users.arguments(schema=CreatePaymentRequestDTO, location='json')
def create_payment(ride_id):
    data = request.json
    result, status_code = user_service.create_payment(ride_id, data)
    return make_response(jsonify(result), status_code)

@users.route("/logout", methods=['POST'])
@jwt_required_with_role('user')
def logout():
    return jsonify({'message': 'Successfully logged out'}), 200
