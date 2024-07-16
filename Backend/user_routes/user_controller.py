import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask_smorest import Blueprint
from flask import jsonify, redirect, url_for
from flask_login import current_user, login_required, logout_user
from decorators.decorators import role_required
from user_routes.dto.requests.user_request import (
    LoginRequestDTO, OrderRideRequestDTO, CalculatePriceRequestDTO, 
    CreatePaymentRequestDTO, ExecutePaymentRequestDTO
)

from user_routes.dto.responses.user_response import (
    LoginResponseDTO, OrderRideResponseDTO, OrderConfirmationResponseDTO, 
    OrderStatusResponseDTO, CalculatePriceResponseDTO, PayResponseDTO, 
    CreatePaymentResponseDTO, ExecutePaymentResponseDTO
)

from user_routes.user_service import UsersService

users_blp = Blueprint("users", "users", url_prefix="/users", description="users routes")

@users_blp.route('/login', methods=['POST'])
@users_blp.arguments(schema=LoginRequestDTO, location='json')
@users_blp.response(status_code=200, schema=LoginResponseDTO)
def user_login(data):
    if current_user.is_authenticated:
        role_dashboard_map = {
            'admin': 'admin_dashboard',
            'user': 'user_dashboard',
            'driver': 'driver_dashboard'
        }
        role = current_user.role
        if role in role_dashboard_map:
            return redirect(url_for(role_dashboard_map[role]))
        else:
            return jsonify({'error': 'Invalid role'}), 400

    result = UsersService.login(data)
    if 'error' in result:
        return jsonify(result), 401
    return jsonify(result), 200

@users_blp.route('/dashboard', methods=['GET'])
@login_required
@role_required("user")
@users_blp.response(status_code=200, schema=LoginResponseDTO)
def dashboard():
    return {'message': 'Welcome to the user dashboard'}

@users_blp.route('/order_ride', methods=['POST'])
@login_required
@role_required("user")
@users_blp.arguments(schema=OrderRideRequestDTO, location='json')
@users_blp.response(status_code=201, schema=OrderRideResponseDTO)
def order_ride(data):
    result = UsersService.order_ride(data, current_user.id)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201

@users_blp.route('/order_confirmation/<ride_id>', methods=['GET'])
@login_required
@role_required('user')
@users_blp.response(status_code=200, schema=OrderConfirmationResponseDTO)
def order_confirmation(ride_id):
    result = UsersService.order_confirmation(ride_id, current_user.id)
    if 'error' in result:
        return jsonify(result), 403
    return jsonify(result), 200

@users_blp.route('/order_status', methods=['GET'])
@login_required
@role_required('user')
@users_blp.response(status_code=200, schema=OrderStatusResponseDTO(many=True))
def order_status():
    result = UsersService.order_status(current_user.id)
    return jsonify(result), 200

@users_blp.route('/calculate_price', methods=['POST'])
@login_required
@role_required("user")
@users_blp.arguments(schema=CalculatePriceRequestDTO, location='json')
@users_blp.response(status_code=200, schema=CalculatePriceResponseDTO)
def calculate_price(data):
    result = UsersService.calculate_price(data)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

@users_blp.route('/order_status/<ride_id>', methods=['GET'])
@login_required
@role_required('user')
@users_blp.response(status_code=200, schema=OrderStatusResponseDTO)
def order_status_detail(ride_id):
    result = UsersService.order_status_detail(ride_id, current_user.id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result), 200

@users_blp.route('/pay/<ride_id>', methods=['GET'])
@login_required
@role_required('user')
@users_blp.response(status_code=200, schema=PayResponseDTO)
def pay(ride_id):
    result = UsersService.pay(ride_id, current_user.id)
    if 'error' in result:
        return jsonify(result), 403
    return jsonify(result), 200

@users_blp.route('/create_payment/<ride_id>', methods=['POST'])
@login_required
@role_required('user')
@users_blp.arguments(schema=CreatePaymentRequestDTO, location='json')
@users_blp.response(status_code=200, schema=CreatePaymentResponseDTO)
def create_payment(ride_id, data):
    result = UsersService.create_payment(ride_id, data)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

@users_blp.route('/execute_payment/<ride_id>', methods=['POST'])
@login_required
@role_required('user')
@users_blp.arguments(ExecutePaymentRequestDTO, location='json')
@users_blp.response(status_code=200, schema=ExecutePaymentResponseDTO)
def execute_payment(ride_id, data):
    result = UsersService.execute_payment(ride_id, data)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

@users_blp.route("/logout", methods=['POST'])
@login_required
@role_required("user")
@users_blp.response(status_code=200, schema=LoginResponseDTO)
def logout():
    logout_user()
    return {'message': 'Successfully logged out'}
