import os

from flask import jsonify,request
from flask_smorest import Api
from Backend.config.models import app, db, InvitationEmails,User
from flask_jwt_extended import decode_token
from Backend.forms import RegistrationForm

from Backend.admin_routes.admin_controller import admins  # Import admin blueprint
from Backend.user_routes.user_controller import users_blp  # Import user blueprint
from Backend.driver_routes.driver_controller import drivers  # Import driver blueprint



class APIConfig:
  API_TITLE = "RideShare App v1"
  API_VERSION = "v1"  
  OPENAPI_VERSION = "3.0.2"
  OPENAPI_URL_PREFIX = "/"
  OPENAPI_SWAGGER_UI_PATH = "/docs"
  OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  SECRET_KEY = os.getenv('API_SECRET_KEY')


app.config.from_object(APIConfig)

api = Api(app)

api.register_blueprint(admins, url_prefix='/admins')  # Register admin routes under /admins
api.register_blueprint(users_blp, url_prefix='/users')  # Register user routes under /users
api.register_blueprint(drivers, url_prefix='/drivers')  # Register driver routes under /drivers

@app.route("/")
def index():
    return jsonify({'message': 'Welcome to the API'})

@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    try:
        token_data = decode_token(token)
        email = token_data['sub']['email']
        role = token_data['sub']['role']
    except Exception as e:
        return jsonify({'message': 'Invalid token', 'error': str(e)}), 400

    db_emails = [inv.email for inv in InvitationEmails.query.all()]

    if email not in db_emails:
        return jsonify({'message': 'Invalid link'}), 400

    data = request.get_json()
    form = RegistrationForm(data=data)
    existing_user = User.query.filter_by(email=email).first()

    if form.validate_on_submit():
        if existing_user:
            return jsonify({'message': 'Error. Email already exists'}), 400
        
        if email == form.email.data:
            if role == 'admin':
                user = User(username=form.username.data, email=form.email.data, password=form.password.data, name=form.name.data, surname=form.surname.data, role='admin')
            elif role == 'driver':
                user = User(username=form.username.data, email=form.email.data, password=form.password.data, name=form.name.data, surname=form.surname.data, role='driver')
            else:
                user = User(username=form.username.data, email=form.email.data, name=form.name.data, password=form.password.data, surname=form.surname.data, role='user')

            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': f'You are now a registered {role}'}), 201

    return jsonify({'errors': form.errors}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')