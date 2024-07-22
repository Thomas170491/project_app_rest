import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask_smorest import Blueprint
from flask import jsonify, redirect, url_for,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import current_user, login_required, logout_user
from Backend.utils.decorators import role_required
from marshmallow.exceptions import ValidationError
import requests
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

user_service = UsersService()

@users_blp.route('/login', methods=['GET'])
def login_form():
    return jsonify({"message": "Please submit your login credentials via POST request to this endpoint."})


@users_blp.route('/login', methods=['POST'])
@users_blp.arguments(schema=LoginRequestDTO, location='json')
@users_blp.response(status_code=200, schema=LoginResponseDTO)
def user_login(data):
    if current_user.is_authenticated:
        role_dashboard_map = {
            'admin': 'admin.dashboard',
            'user': 'users.dashboard',
            'driver': 'drivers.dashboard'
        }
        role = current_user.role
        if role in role_dashboard_map:
            return redirect(url_for (role_dashboard_map[role]))
        else:
            return jsonify({'error': 'Invalid role'}), 400

    result = user_service.login(data)
    if 'error' in result:
        return jsonify(result), 401
    return jsonify(result), 200

@users_blp.route('/dashboard', methods=['GET'])
@login_required
@role_required("user")
@jwt_required
@users_blp.response(status_code=200, schema=LoginResponseDTO)
def dashboard():
    current_user = get_jwt_identity()
    return {'message': f'Welcome {current_user}'}
    

@users_blp.route('/order_ride', methods=['POST'])
@login_required
@role_required("user")
@users_blp.arguments(schema=OrderRideRequestDTO, location='json')
@users_blp.response(status_code=201, schema=OrderRideResponseDTO)
def order_ride(data):
    result = user_service.order_ride(data, current_user.id)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201

@users_blp.route('/order_confirmation/<ride_id>', methods=['GET'])
@login_required
@role_required('user')
@users_blp.response(status_code=200, schema=OrderConfirmationResponseDTO)
def order_confirmation(ride_id):
    result = user_service.order_confirmation(ride_id, current_user.id)
    if 'error' in result:
        return jsonify(result), 403
    return jsonify(result), 200


@users_blp.route('/calculate_price', methods=['POST'])
@login_required
@role_required("user")
@users_blp.arguments(schema=CalculatePriceRequestDTO, location='json')
@users_blp.response(status_code=200, schema=CalculatePriceResponseDTO)
def calculate_price(data):
    result = user_service.calculate_price(data)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

@users_blp.route('/order_status/<ride_id>', methods=['GET'])
@login_required
@role_required('user')
#@users_blp.arguments(Or)
@users_blp.response(status_code=200, schema=OrderStatusResponseDTO)
def order_status_detail(ride_id):
    result = user_service.order_status_detail(ride_id, current_user.id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result), 200

@users_blp.route('/pay/<ride_id>', methods=['GET'])
@login_required
@role_required('user')
@users_blp.response(status_code=200, schema=PayResponseDTO)
def pay(ride_id):
    result = user_service.pay(ride_id, current_user.id)
    if 'error' in result:
        return jsonify(result), 403
    return jsonify(result), 200

@users_blp.route('/create_payment/<ride_id>', methods=['POST'])
@login_required
@role_required('user')
@users_blp.arguments(schema=CreatePaymentRequestDTO, location='json')
@users_blp.response(status_code=200, schema=CreatePaymentResponseDTO)
def create_payment(ride_id):
    # Extract JSON data from request
    data = request.json
    
    # Validate JSON data using schema if needed
    # Example: validation_result = CreatePaymentRequestDTO.validate(data)
    # if validation_result.errors:
    #     return jsonify(validation_result.errors), 400
    
    # Call your service function with both ride_id and data
    result = user_service.create_payment(ride_id, data)
    
    # Handle the result
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 200

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


@users_blp.route("/logout", methods=['POST'])
@login_required
@role_required("user")
@users_blp.response(status_code=200, schema=LoginResponseDTO)
def logout():
    logout_user()
    return {'message': 'Successfully logged out'}
