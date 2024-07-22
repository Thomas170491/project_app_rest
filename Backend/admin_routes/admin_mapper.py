import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from Backend.config.models import InvitationEmails

class AdminMapper:
    def map_to_invitation(self, data):
        return InvitationEmails(
            email=data['email'],
            token=data['token']
        ).to_dict()

    def map_to_user_list(self, users):
        return [user for user in users]