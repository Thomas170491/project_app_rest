import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from admin_repository import AdminRepository
from admin_mapper import AdminMapper
from flask_jwt_extended import create_access_token
from Backend.config.models import generate_deeplink, send_invitation_email

class AdminService:
    def __init__(self):
        self.repository = AdminRepository()
        self.mapper = AdminMapper()

    def send_link(self, email, role):
        token = create_access_token(identity={'email': email, 'role': role})
        deeplink = generate_deeplink(email, token)
        invite_data = self.mapper.map_to_invitation({'email': email, 'token': token})
        self.repository.add_invitation_email(invite_data)
        send_invitation_email(email, deeplink)
        return {'message': 'Invitation sent successfully!'}

    def get_dashboard_data(self):
        users = self.repository.get_all_users_by_role('user')
        drivers = self.repository.get_all_users_by_role('driver')
        admins = self.repository.get_all_users_by_role('admin')
        return {
            'users': self.mapper.map_to_user_list(users),
            'drivers': self.mapper.map_to_user_list(drivers),
            'admins': self.mapper.map_to_user_list(admins)
        }

    def delete_user(self, user_id):
        self.repository.delete_user(user_id)
        return {'message': 'User deleted successfully'}

    def edit_user_role(self, user_id, new_role):
        self.repository.update_user_role(user_id, new_role)
        return {'message': 'User role updated successfully'}
