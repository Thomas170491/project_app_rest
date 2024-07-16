import os
from flask import Flask
from firebase_admin import credentials,firestore,initialize_app,_apps
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS



# Load environment variables
load_dotenv()


# Initialize Firebase Admin SDK with service account


def get_firestore_client():
    if not _apps:
        cred = credentials.Certificate(os.getenv('FIREBASE_KEY_FILE'))
        initialize_app(cred)
    return firestore.client()

db = get_firestore_client()

# Initialize Firestore
db = firestore.client()

# Initialize extensions


def create_app():

    
    app= Flask(__name__, instance_relative_config=True)
    

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['PAYPAL_CLIENT_ID'] = os.getenv('PAYPAL_CLIENT_ID')
    app.config['PAYPAL_CLIENT_SECRET'] = os.getenv('PAYPAL_CLIENT_SECRET')
    app.config['PAYPAL_API_BASE'] = 'https://api.sandbox.paypal.com'
    
    return app



app = create_app()


login_manager = LoginManager(app)
mail = Mail(app)
jwt = JWTManager(app)
cors = CORS(app)



class User(UserMixin):
    def __init__(self, username, name, surname, email, password, role):
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def to_dict(self):
        return {
            'username': self.username,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role 
            }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.id}>'

class RideOrder:
    def __init__(self, name, departure, destination, time, price, user_id=None):
        self.name = name
        self.departure = departure
        self.destination = destination
        self.time = time
        self.status = 'pending'
        self.price = price
        self.user_id = user_id

    def to_dict(self):
        return {
            'name': self.name,
            'departure': self.departure,
            'destination': self.destination,
            'time': self.time,
            'status': self.status,
            'price': self.price,
            'user_id': self.user_id
        }

    def save(self):
        ride_order_ref = db.collection('ride_orders').document()
        ride_order_ref.set(self.to_dict())
        self.id = ride_order_ref.id  # Store the document ID

    @staticmethod
    def get_by_id(order_id):
        ride_order_ref = db.collection('ride_orders').document(order_id)
        ride_order_data = ride_order_ref.get()
        if ride_order_data.exists:
            return RideOrder(**ride_order_data.to_dict())
        return None

    @staticmethod
    def get_all():
        ride_orders_ref = db.collection('ride_orders')
        return [RideOrder(**ro.to_dict()) for ro in ride_orders_ref.stream()]

    def __repr__(self):
        return f'<RideOrder {self.id}>'

class InvitationEmails:
    def __init__(self, email, token):
        self.email = email
        self.token = token

    def to_dict(self):
        return {
            'email': self.email,
            'token': self.token
        }

    def save(self):
        invitation_ref = db.collection('invitation_emails').document()
        invitation_ref.set(self.to_dict())
        self.id = invitation_ref.id  # Store the document ID

    @staticmethod
    def get_all():
        invitations_ref = db.collection('invitation_emails')
        return [InvitationEmails(**ie.to_dict()) for ie in invitations_ref.stream()]

    def __repr__(self):
        return f'<InvitationEmails {self.id}>'
class Vehicle:
    def __init__(self, make, model, year, category, driver_id):
        self.make = make
        self.model = model
        self.year = year
        self.category = category
        self.driver_id = driver_id

    def to_dict(self):
        return {
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'category': self.category,
            'driver_id': self.driver_id
        }

    def save(self):
        vehicle_ref = db.collection('vehicles').document()
        vehicle_ref.set(self.to_dict())
        self.id = vehicle_ref.id  # Store the document ID

    @staticmethod
    def get_by_id(vehicle_id):
        vehicle_ref = db.collection('vehicles').document(vehicle_id)
        vehicle_data = vehicle_ref.get()
        if vehicle_data.exists:
            return Vehicle(**vehicle_data.to_dict())
        return None

    @staticmethod
    def get_all():
        vehicles_ref = db.collection('vehicles')
        return [Vehicle(**v.to_dict()) for v in vehicles_ref.stream()]

    def __repr__(self):
        return f'<Vehicle {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))







def generate_deeplink(email, token):
    return f"http://127.0.0.1:5000/register/{token}"

def send_invitation_email(email, deeplink):
    subject = "Invitation à rejoindre notre service VTC"
    body = f"""
    Bonjour,
    
    Vous avez été invitée à rejoindre notre service VTC. Cliquez sur le lien ci-dessous pour créer votre compte :
    
    {deeplink}
    
    Cordialement,
    L'équipe VTC
    """
    
    msg = Message(subject, sender='thomaspapas470@gmail.com', recipients=[email])
    msg.body = body

    with app.app_context():
        mail.send(msg)







if __name__ == '__main__':
    app.run(debug=True)