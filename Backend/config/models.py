from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
jwt = JWTManager()
cors = CORS()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    gender = db.Column(db.String(50), default="female")
    role = db.Column(db.String(10))
    vehicles = db.relationship('Vehicle', backref='driver', lazy=True)

    def __init__(self, username, name, surname, email, password, role):
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.role = role
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.id}>'

class RideOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    departure = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    time = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # Ride status
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # ID of the user who accepts the ride
    price = db.Column(db.Float, nullable=False)
    
    user = db.relationship('User', backref='ride_orders', lazy=True, foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<RideOrder {self.id}>'

class InvitationEmails(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    token = db.Column(db.String(128))

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'category': self.category
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    with app.app_context():
        db.create_all()

    return app