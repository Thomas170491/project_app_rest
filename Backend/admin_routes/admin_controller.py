import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from flask import request, jsonify
from flask_login import logout_user, login_required
from flask_smorest import Blueprint
from admin_service import AdminService
from decorators.decorators import role_required
from dto.requests import SendLinkRequestDTO
from dto.responses import SendLinkResponseDTO

admins = Blueprint("admins", "admins", url_prefix="/admins", description="admin routes")

admin_service = AdminService()

@admins.route('/send_link', methods=['POST'])
@login_required
@role_required('admin')
def send_link():
    data = request.get_json()
    form = SendLinkRequestDTO().load(data)
    response = admin_service.send_link(form['email'], form['role'])
    return SendLinkResponseDTO().dump(response), 200

@admins.route("/dashboard", methods=['GET'])
@login_required
@role_required("admin")
def dashboard():
    response = admin_service.get_dashboard_data()
    return jsonify(response), 200

@admins.route("/delete-user/<user_id>", methods=['DELETE'])
@login_required
@role_required("admin")
def delete_user(user_id):
    response = admin_service.delete_user(user_id)
    return jsonify(response), 200

@admins.route("/edit-user/<user_id>", methods=['PATCH'])
@login_required
@role_required("admin")
def edit_user(user_id):
    data = request.get_json()
    new_role = data.get('role', 'user')
    response = admin_service.edit_user_role(user_id, new_role)
    return jsonify(response), 200

@admins.route("/logout", methods=['POST'])
@login_required
@role_required("admin")
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
