from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,EmailField
from wtforms.validators import  DataRequired, Email, EqualTo, ValidationError,Length,InputRequired
from config.models import User 


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
    
    
    
class OrderRide(FlaskForm) :
    name = StringField("Name", validators=[DataRequired()])
    departure = StringField("Departure", validators = [DataRequired()])
    destination = StringField("Destination", validators = [DataRequired()])
    time= StringField("I want the driver to arrive at :", validators = [DataRequired()])
    submit = SubmitField("Order Ride")
    
    
    


    