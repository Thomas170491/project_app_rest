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
    departure = StringField("Departure", validators=[DataRequired()])
    destination = StringField("Destination", validators=[DataRequired()])
    time = StringField("I want the driver to arrive at:", validators=[DataRequired()])
    price = DecimalField("Estimated Price")
    submit = SubmitField("Order Ride")

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
    