import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import  jsonify
from flask_login import login_required, current_user,logout_user
from flask_smorest import Blueprint
from driver_routes.driver_service import DriverService
from decorators.decorators import role_required
from dto.requests.requests import AcceptRideRequestDTO, DeclineRideRequestDTO
from dto.responses.responses import (
    DashboardResponseDTO, DisplayRidesResponseDTO, AcceptRideResponseDTO, DeclineRideResponseDTO
)

drivers_blp = Blueprint("drivers", "drivers", url_prefix="/drivers", description="drivers routes")

driver_service = DriverService()

@drivers_blp.route("/dashboard", methods=["GET"])
@login_required
@role_required("driver")
def dashboard():
    response = driver_service.get_dashboard()
    return DashboardResponseDTO().dump(response), 200

@drivers_blp.route("/display_rides", methods=["GET"])
@login_required
@role_required('driver')
def display_rides():
    response = driver_service.display_rides()
    return jsonify(DisplayRidesResponseDTO(many=True).dump(response)), 200

@drivers_blp.route("/accept_ride/<int:ride_id>", methods=['POST'])
@login_required
@role_required('driver')
def accept_ride(ride_id):
    driver_id = current_user.id
    response = driver_service.accept_ride(ride_id, driver_id)
    if 'error' in response:
        return jsonify({'error': response['error']}), 400
    return AcceptRideResponseDTO().dump(response), 200

@drivers_blp.route("/decline_ride/<int:ride_id>", methods=['POST'])
@login_required
@role_required('driver')
def decline_ride(ride_id):
    driver_id = current_user.id
    response = driver_service.decline_ride(ride_id, driver_id)
    if 'error' in response:
        return jsonify({'error': response['error']}), 400
    return DeclineRideResponseDTO().dump(response), 200

@drivers_blp.route("/logout", methods=['POST'])
@login_required
@role_required("driver")
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
