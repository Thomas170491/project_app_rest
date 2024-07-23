import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from flask import request, jsonify
from flask_smorest import Blueprint
from admin_routes.admin_service import AdminService
from admin_routes.dto.requests import SendLinkRequestDTO
from admin_routes.dto.responses import SendLinkResponseDTO
from Backend.utils.decorators import jwt_required_with_role
admins = Blueprint("admins", "admins", url_prefix="/admins", description="admin routes")

admin_service = AdminService()


@admins.route('/send_link', methods=['POST'])
@jwt_required_with_role('admin')
def send_link():
    data = request.get_json()
    form = SendLinkRequestDTO().load(data)
    response = admin_service.send_link(form['email'], form['role'])
    return SendLinkResponseDTO().dump(response), 200

@admins.route("/dashboard", methods=['GET'])
@jwt_required_with_role("admin")
def dashboard():
    response = admin_service.get_dashboard_data()
    return jsonify(response), 200

@admins.route("/delete-user/<user_id>", methods=['DELETE'])
@jwt_required_with_role("admin")
def delete_user(user_id):
    response = admin_service.delete_user(user_id)
    return jsonify(response), 200

@admins.route("/edit-user/<user_id>", methods=['PATCH'])
@jwt_required_with_role("admin")
def edit_user(user_id):
    data = request.get_json()
    new_role = data.get('role', 'user')
    response = admin_service.edit_user_role(user_id, new_role)
    return jsonify(response), 200

@admins.route("/logout", methods=['POST'])
@jwt_required_with_role("admin")
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200