

from flask import  render_template,flash,redirect,url_for
from config.models import app,db, InvitationEmails,User
from flask_jwt_extended import decode_token
from forms import RegistrationForm

from admin_routes.admin_controller import admins  # Import admin blueprint
from user_routes.user_controller import users  # Import user blueprint
from driver_routes.driver_controller import drivers  # Import driver blueprint

app.register_blueprint(admins, url_prefix='/admins')  # Register admin routes under /admins
app.register_blueprint(users, url_prefix='/users')  # Register user routes under /users
app.register_blueprint(drivers, url_prefix='/drivers')  # Register driver routes under /drivers


@app.route("/")
def index():
    return render_template('base.html')


@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token):

        try:

            # Decode the token to extract user information
            token_data = decode_token(token)

            # Extract the email and role from the decoded token data
            email = token_data['sub']['email']
            role = token_data['sub']['role']
        except Exception as e:
            # If an error occurs during token decoding (e.g., token is invalid or expired),
            # flash an error message to the user indicating that the token is invalid
            flash('Invalid token', 'danger')

            # Redirect the user to the home page (index) as the token is invalid
            return redirect(url_for('index'))

        # Fetch all invitation emails from the database
        db_emails = [inv.email for inv in InvitationEmails.query.all()]

        # Check if the email extracted from the token is in the list of invitation emails
        if email not in db_emails:
            # If the email is not in the invitation emails, show an error message
            flash('Invalid link', 'danger')
            
            # Redirect the user to the home page (index) as the link is invalid
            return redirect(url_for('index'))
        
        # Create a new instance of the registration form
        form = RegistrationForm()
        existing_user = User.query.filter_by(email=email).first()

        # Check if the form has been submitted and is valid
        if form.validate_on_submit():
            if existing_user:
                flash('Error. Email already exists')
                return redirect(url_for(inde))
            # Verify that the email provided in the form matches the email extracted from the token
            if email == form.email.data: 
                # Create a new user instance based on the role extracted from the token
                if role == 'admin':
                    user = User(username=form.username.data, email=form.email.data, password=form.password.data, name=form.name.data, surname=form.surname.data, role='admin')
                elif role == 'driver':
                    user = User(username=form.username.data, email=form.email.data, password=form.password.data, name=form.name.data, surname=form.surname.data, role='driver')
                else:
                    user = User(username=form.username.data, email=form.email.data, name=form.name.data, password=form.password.data, surname=form.surname.data, role='user')

                # Set the user's password
                user.set_password(form.password.data)

                # Add the new user to the database session
                db.session.add(user)

                # Commit the session to save the user to the database
                db.session.commit()

                # Flash a success message indicating that the user is now registered
                flash(f'You are now a registered {role}', 'success')

                # Redirect the user to the login page 
                return redirect(url_for('users.user_login'))

        # Render the registration template with the form and email context variables
        return render_template('register.html', form=form, email=email)


# Run the application
if __name__ == "__main__":
    
    app.run(debug=True, host='0.0.0.0')