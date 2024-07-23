import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint
from Backend.driver_routes.driver_service import DriverService
from driver_routes.dto.requests.requests import AcceptRideRequestDTO, DeclineRideRequestDTO
from driver_routes.dto.responses.responses import (
    DashboardResponseDTO, DisplayRidesResponseDTO, AcceptRideResponseDTO, DeclineRideResponseDTO
)
from Backend.utils.decorators import jwt_required_with_role  # Import your custom decorator

drivers_blp = Blueprint("drivers", "drivers", url_prefix="/drivers", description="drivers routes")

driver_service = DriverService()

@drivers_blp.route("/dashboard", methods=["GET"])
@jwt_required_with_role("driver")
def dashboard():
    response = driver_service.get_dashboard()
    return DashboardResponseDTO().dump(response), 200

@drivers_blp.route("/display_rides", methods=["GET"])
@jwt_required_with_role('driver')
def display_rides():
    response = driver_service.display_rides()
    return jsonify(DisplayRidesResponseDTO(many=True).dump(response)), 200

@drivers_blp.route("/accept_ride/<int:ride_id>", methods=['POST'])
@jwt_required_with_role('driver')
def accept_ride(ride_id):
    driver_id = get_jwt_identity().get('id')  # Adjust to get driver ID from JWT
    response = driver_service.accept_ride(ride_id, driver_id)
    if 'error' in response:
        return jsonify({'error': response['error']}), 400
    return AcceptRideResponseDTO().dump(response), 200

@drivers_blp.route("/decline_ride/<int:ride_id>", methods=['POST'])
@jwt_required_with_role('driver')
def decline_ride(ride_id):
    driver_id = get_jwt_identity().get('id')  # Adjust to get driver ID from JWT
    response = driver_service.decline_ride(ride_id, driver_id)
    if 'error' in response:
        return jsonify({'error': response['error']}), 400
    return DeclineRideResponseDTO().dump(response), 200

@drivers_blp.route("/logout", methods=['POST'])
@jwt_required_with_role("driver")
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200
