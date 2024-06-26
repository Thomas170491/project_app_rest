import os
import sys 
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.models import  db 
from flask import request, render_template, flash, redirect, url_for, abort,jsonify
from config.models import User, RideOrder
from werkzeug.urls import url_parse
from forms import  LoginForm, OrderRide
from flask_login import current_user, login_user, logout_user, login_required
from flask_smorest import Blueprint
from decorators.decorators import role_required
from user_routes.user_service import calculate_price,get_paypal_access_token
import requests


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
@login_required
@role_required("user")
def order_ride():
    form = OrderRide()
    if form.validate_on_submit():
        price = calculate_price(str(form.departure.data), str(form.destination.data))
        if form.name.data != request.form['name'] or \
          form.departure.data != request.form['departure'] or \
           form.destination.data != request.form['destination'] or \
           form.time.data != request.form['time']:
           flash("Form data has been tampered with. Please try again.", 'danger')
           return redirect(url_for('users.order_ride'))
        
        if not isinstance(price, (int, float)):
            raise ValueError("Calculated price is not a valid number")

        order = RideOrder(
                name=form.name.data,
                departure=form.departure.data,
                destination= form.destination.data,
                time=form.time.data,
                user_id=current_user.id,
                price= price 
            )
        
            
        db.session.add(order)
        db.session.commit()
        flash("Your ride is on the way", 'success')
        return redirect(url_for('users.pay', 
                                    name=form.name.data,
                                    departure=form.departure.data,
                                    destination= form.destination.data,
                                    time=form.time.data,
                                    ride_id=order.id,
                                    price=calculate_price(form.departure.data, form.destination.data)))
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
    current_user_id = current_user.id
    rides = RideOrder.query.filter_by(user_id=current_user_id).all()
    return render_template('rides_status.html', rides=rides)  

@users.route('/calculate_price', methods=['GET','POST'])
@login_required
@role_required("user")
def calculated_price():
    # Check if the request contains JSON data
    if request.is_json:
        # Parse JSON data from the request body
        data = request.json
        
        # Extract departure and destination addresses from the JSON data
        departure_address = data.get('departure')
        destination_address = data.get('destination')
        
        # Perform price calculation logic here based on the departure and destination addresses
        # For demonstration purposes, let's just return a dummy price
        price = calculate_price(departure_address,destination_address)
        
        # Return the calculated price as JSON response
        return jsonify({'price': price}), 200
    else:
        # If the request does not contain JSON data, return an error response
        return jsonify({'error': 'Request body must be JSON'}), 400

                            

@users.route('/order_status/<int:ride_id>')
@login_required
@role_required('user')   
def order_status(ride_id):
    # Retrieve the ride order by ride_id
    ride_order = RideOrder.query.get(ride_id)
    print(ride_order.user_id)
    print(current_user.id)


    # Check if the ride order exists and belongs to the current user
    if ride_order is None or ride_order.user_id != current_user.id:
        abort(404)

    # Get the status of the ride order
    ride_status = ride_order.status

    # Render a template to display the status to the user
    return render_template('order_status.html', ride_status=ride_status)



# Route for rendering the payment page

@users.route('/pay/<int:ride_id>', methods=['GET'])
@login_required
@role_required('user')
def pay(ride_id):
    # Retrieve the ride order by ride_id
    ride_order = RideOrder.query.get_or_404(ride_id)

    # Ensure the ride order belongs to the current user
    if ride_order.user_id != current_user.id:
        abort(403)

    # Pass the ride details to the template
    return render_template('payment.html', 
                           ride_id=ride_id, 
                           name=ride_order.name,
                           departure=ride_order.departure,
                           destination=ride_order.destination,
                           time=ride_order.time,
                           client_id=os.getenv('PAYPAL_CLIENT_ID'))


# Route for creating a PayPal payment
@users.route('/create_payment/<int:ride_id>', methods=['POST'])
@login_required  # Ensure user is logged in
@role_required('user')  # Ensure user has the 'user' role
def create_payment(ride_id):
    # Obtain PayPal access token
    access_token = get_paypal_access_token()
    
    # Get the departure and destination addresses from the request data (assuming they are submitted via a form)
    departure_address = request.form.get('departure')
    destination_address = request.form.get('destination')
    
    # Calculate the total payment amount based on the departure and destination addresses
    total_amount = calculate_price(departure_address, destination_address)
    
    # Construct payment data with the dynamically calculated total amount
    payment_data = {
        "intent": "sale",  # Payment intent (sale, authorize, order)
        "redirect_urls": {
            "return_url": url_for('users.execute_payment', ride_id=ride_id, _external=True),  # URL to redirect after payment execution
            "cancel_url": url_for('users.pay', ride_id=ride_id, _external=True),  # URL to redirect if payment is canceled
        },
        "payer": {
            "payment_method": "paypal"  # Payment method (paypal, credit_card)
        },
        "transactions": [{
            "amount": {
                "total": str(total_amount),  # Total amount of the payment (converted to string)
                "currency": "USD"  # Currency code (USD, EUR, etc.)
            },
            "description": "Ride Payment"  # Payment description
        }]
    }

    # Make a POST request to create the payment
    response = requests.post(
        f"{os.getenv('PAYPAL_API_BASE')}/v1/payments/payment",  # PayPal Payments API endpoint
        json=payment_data,  # Payment data in JSON format
        headers={
            "Content-Type": "application/json",  # Specify content type as JSON
            "Authorization": f"Bearer {access_token}",  # Include access token in the authorization header
        }
    )

    # Extract payment information from the response
    payment = response.json()
    # Redirect user to PayPal approval URL
    for link in payment['links']:
        if link['rel'] == 'approval_url':
            return redirect(link['href'])

    # If payment creation failed, display an error message
    return "Error creating payment"

# Route for executing a PayPal payment
@users.route('/execute_payment/<int:ride_id>', methods=['GET'])
@login_required  # Ensure user is logged in
@role_required('user')  # Ensure user has the 'user' role
def execute_payment(ride_id):
    # Retrieve payment ID and payer ID from query parameters
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    
    # Obtain PayPal access token
    access_token = get_paypal_access_token()

    # Make a POST request to execute the payment
    response = requests.post(
        f"{os.getenv('PAYPAL_API_BASE')}/v1/payments/payment/{payment_id}/execute",  # PayPal execute payment endpoint
        json={"payer_id": payer_id},  # Include payer ID in JSON format
        headers={
            "Content-Type": "application/json",  # Specify content type as JSON
            "Authorization": f"Bearer {access_token}",  # Include access token in the authorization header
        }
    )

    # Extract payment execution result from the response
    payment = response.json()

    # If payment execution is successful, display a success message
    if payment['state'] == 'approved':
        flash('Payment successful!', 'success')
        return redirect(url_for('users.order_confirmation', ride_id=ride_id))  # Redirect to order confirmation page
    # If payment execution failed, display a failure message
    else:
        flash('Payment failed. Please try again.', 'danger')
        return redirect(url_for('users.pay', ride_id=ride_id))  # Redirect back to payment page

    

@users.route("/logout")
@login_required
@role_required("user")
def logout():
  logout_user()
  return redirect(url_for("users.user_login"))