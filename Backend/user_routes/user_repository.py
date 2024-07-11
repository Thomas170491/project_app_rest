import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))



from config.models import db, User, RideOrder


class UsersRepository:

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def add_order(order):
        db.session.add(order)
        db.session.commit()

    @staticmethod
    def get_ride_order(ride_id):
        return RideOrder.query.get(ride_id)

    @staticmethod
    def get_ride_orders_by_user(user_id):
        return RideOrder.query.filter_by(user_id=user_id).all()
