import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from Backend.config.models import User, InvitationEmails,db

class AdminRepository:
    def __init__(self):
        self.users_ref = db.collection('users')
        self.invites_ref = db.collection('invitation_emails')

    def add_invitation_email(self, invite_data):
        self.invites_ref.add(invite_data)

    def get_all_users_by_role(self, role):
        query = self.users_ref.where('role', '==', role).stream()
        users = []
        for doc in query:
            user = doc.to_dict()
            user['id'] = doc.id
            users.append(user)
        return users

    def delete_user(self, user_id):
        user_ref = self.users_ref.document(user_id)
        user_ref.delete()

    def update_user_role(self, user_id, new_role):
        user_ref = self.users_ref.document(user_id)
        user_ref.update({'role': new_role})