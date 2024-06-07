import os
import sys 
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.models import  db 
from flask import request, render_template, flash, redirect, url_for, abort
from config.models import User, RideOrder
from werkzeug.urls import url_parse
from forms import  LoginForm, OrderRide
from flask_login import current_user, login_user, logout_user, login_required
from flask_smorest import Blueprint
from decorators.decorators import role_required
from user_routes.user_service import calculate_price

users = Blueprint("users", "users", url_prefix="/users", description="users routes")

@users.route('/login', methods=['GET', 'POST'])
def user_login():
    # Check if current_user is logged in, if so redirect to a page that makes sense
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    
    form = LoginForm()  # Creation of a form
    
    if form.validate_on_submit():  # Verify if the form is valid
        # Check that user is in User
        user = User.query.filter_by(username=form.username.data).first()  # Do a query on users, filter the result by the username provided in the form and give me the first result
        if user and user.check_password(form.password.data):  # Verify if the user exists and if the password given is valid
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':  # Check if next_page URL is a relative URL
            
                next_page = url_for(f'{current_user.role}s.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password', 'danger')  # If the user doesn't exist or the password is invalid
            return redirect(url_for('users.user_login'))
 
    return render_template('user_login.html', title = 'Sign In', form = form) #if login fails
 
@users.route('/dashboard')
@login_required
@role_required("user")
def dashboard():
  return render_template('user_dashboard.html')


@users.route('/order_ride', methods=['GET', 'POST'])
@login_required  # Protecting our pages
@role_required("user")
def order_ride():
    form = OrderRide()
    if form.validate_on_submit():
        # Form data is valid, proceed with further processing
            try:
                price = calculate_price(form.departure.data, form.destination.data)
            except Exception as e:
                flash("Failed to calculate price. Please try again.", 'danger')
                return redirect(url_for('users.order_ride'))

            order = RideOrder(
                name=form.name.data,
                departure=form.departure.data,
                destination=form.destination.data,
                time=form.time.data,
                user_id=current_user.id,
                price=price
            )
            db.session.add(order)
            db.session.commit()
            flash("Your ride is on the way", 'success')
            return redirect(url_for('users.order_confirmation',
                                    name=form.name.data,
                                    departure=form.departure.data,
                                    destination=form.destination.data,
                                    time=form.time.data,
                                    ride_id=order.id,
                                    price=price))
    return render_template('order_ride.html', form=form)

@users.route('/order_confirmation/<int:ride_id>')
@login_required
@role_required('user')
def order_confirmation(ride_id):
    # Fetch the ride order details by ride_id
    ride_order = RideOrder.query.get_or_404(ride_id)

    # Ensure the ride order belongs to the current user
    if ride_order.user_id != current_user.id:
        abort(403)

   
    name = current_user.name
    departure = ride_order.departure
    destination = ride_order.destination
    time = ride_order.time

    return render_template('order_confirmation.html',
                           ride_id=ride_id,
                           name=name,
                           departure=departure,
                           destination=destination,
                           time=time)
@users.route('/order_status')
@login_required
@role_required('user')
def order_status():
    rides = RideOrder.query.all()
    
    return render_template('rides_status.html', rides=rides)  

@users.route('/calculate_price', methods=['POST'])
@login_required
@role_required("user")
def calculate_price_route():
    data = request.get_json()
    departure = data.get('departure')
    destination = data.get('destination')
    
    if not departure or not destination:
        return {'error': 'Invalid input'}, 400
    
    price = calculate_price(departure, destination)
    
    return {'price': price}
                            

@users.route('/order_status/<int:ride_id>')
@login_required
@role_required('user')   
def order_status(ride_id):
    # Retrieve the ride order by ride_id
    ride_order = RideOrder.query.get(ride_id)

    # Check if the ride order exists and belongs to the current user
    if ride_order is None or ride_order.user_id != current_user.id:
        abort(404)

    # Get the status of the ride order
    ride_status = ride_order.status

    # Render a template to display the status to the user
    return render_template('order_status.html', ride_status=ride_status)

    

@users.route("/logout")
@login_required
@role_required("user")
def logout():
  logout_user()
  return redirect(url_for("users.user_login"))

