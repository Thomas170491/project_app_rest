import os
import sys 

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail,Message
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from _datetime import datetime 


# Initialize extensions

db = SQLAlchemy()  # SQLAlchemy for database interactions
login_manager = LoginManager()  # Flask-Login for user session management
mail = Mail()  # Flask-Mail for email handling
jwt = JWTManager()  # Flask-JWT-Extended for JWT authentication

#Data classes 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    gender = db.Column(db.String(50), default="female")
    role = db.Column(db.String(10))

    def __init__(self, username, name, surname, email, password,role):
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
    departure = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(10), nullable=False,  default=lambda: datetime.utcnow().strftime('%H:%M:%S'))
    status = db.Column(db.String(20), default='pending')  # Ride status
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # ID of the user who accepts the ride
    price = db.Column(db.Integer, nullable = False)
    
    user = db.relationship('User', backref='ride_orders', lazy=True, foreign_keys=[user_id])
    
    ''''''
    
    def __repr__(self):
        return f'<RideOrder {self.id}>'

class InvitationEmails(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    token = db.Column(db.String(128))
# User loader function

'''
The load_user function is defined to load a user from the  User model. 
This function is registered with the LoginManager using the @login_manager.user_loader decorator.
'''
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Flask application
    app = Flask(__name__)

    # Configure the Flask application with necessary settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/nomades/Documents/pse_2024_0405/flask/Project_App/instance/project_app.db'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable track modifications to save resources
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Secret key for session management and CSRF protection
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Secret key for JWT
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Mail server
    app.config['MAIL_PORT'] = 587  # Mail server port
    app.config['MAIL_USE_TLS'] = True  # Use TLS for secure email transmission
    app.config['MAIL_USE_SSL'] = False  # Do not use SSL (we are using TLS)
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Email username from environment variables
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Email password from environment variables
    
    

    # Initialize extensions with the Flask application
    login_manager.init_app(app)  # Initialize Flask-Login
    login_manager.login_view = 'users.user_login'  # Redirect not logged-in users to this page
    db.init_app(app)  # Initialize SQLAlchemy
    mail.init_app(app)  # Initialize Flask-Mail
    jwt.init_app(app)  # Initialize Flask-JWT-Extended

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    
   

    return app

app = create_app()

def generate_deeplink(email, token):
    # Generate the deeplink with the token
    deeplink = f"http://127.0.0.1:5000/register/{token}"
    return deeplink

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
         




'''
with app.app_context(): 
    a1 = User(username='Thomas170491', name='Thomas', surname= 'Papas', email= 'thomaspapas470@gmail.com', password= '0123456789',role = 'admin')
    u1 = User(username='test_user1', name='Test', surname= 'Test', email= 'email2@email.com', password= 'testuser',role='driver')
    d1 = User(username='test1', name='Test', surname= 'Test', email= 'email1@email.com', password= 'testuser', role='user')
    db.session.add(a1)
    db.session.add(d1)
    db.session.add(u1)
    db.session.commit()
'''
'''
with app.app_context(): 
    d1 = Driver(username='test2', name='Test', surname= 'Test', email= 'email10@email.com', password= 'testuser')
    db.session.add(d1)
    db.session.commit()


'''
