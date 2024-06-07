from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,EmailField,DecimalField
from wtforms.validators import  DataRequired, Email, EqualTo, ValidationError,Length,InputRequired
from config.models import User 
from user_routes.user_service import calculate_price


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=50)])
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=50)])
    

class InvitationForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired()])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin'), ('driver', 'Driver')], validators=[InputRequired()])

#Create a form to login a user 
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class OrderRide(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    street_name_departure = StringField('Street Name of your departure', validators=[DataRequired()])
    street_number_departure = StringField('Street Number of your departure', validators=[DataRequired()])
    postal_code_departure = StringField('Postal Code of your departure', validators=[DataRequired()])
    city_departure = StringField('City of your departure', validators=[DataRequired()])
    
    street_name_destination = StringField('Street Name of your destination', validators=[DataRequired()])
    street_number_destination = StringField('Street Number', validators=[DataRequired()])
    postal_code_destination = StringField('Postal Code of your destination', validators=[DataRequired()])
    city_destination = StringField('City of your destination', validators=[DataRequired()])
    time = StringField("I want the driver to arrive at:", validators=[DataRequired()])
    price = DecimalField("Estimated Price")
    submit = SubmitField("Order Ride")
    
    def get_full_departure_address(self):
        # Concatenate the departure address components
        departure_address = f"{self.street_number_departure.data} {self.street_name_departure.data}, {self.postal_code_departure.data} {self.city_departure.data}"
        return departure_address
    
    def get_full_destination_address(self):
        # Concatenate the destination address components
        destination_address = f"{self.street_number_destination.data} {self.street_name_destination.data}, {self.postal_code_destination.data} {self.city_destination.data}"
        return destination_address
    
    @property
    def departure(self):
        # Retrieve the full departure address
        return self.get_full_departure_address()
    
    @property
    def destination(self):
        # Retrieve the full destination address
        return self.get_full_destination_address()

'''
    def validate(self):
        if not super().validate():
            return False

        departure = self.departure.data
        destination = self.destination.data
        if not departure or not destination:
            self.departure.errors.append('Please enter a valid departure location.')
            self.destination.errors.append('Please enter a valid destination location.')
            return False

        try:
            price = calculate_price(departure, destination)
            self.price.data = price
        except Exception as e:
            self.price.errors.append('Failed to calculate price.')
            return False

        return True
'''


  
    