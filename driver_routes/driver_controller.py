import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import render_template, flash, redirect,url_for
from flask_login import current_user,  logout_user, login_required
from flask_smorest import Blueprint
from config.models import  db,RideOrder
from decorators.decorators import role_required
from datetime import datetime 

drivers = Blueprint("drivers", "drivers", url_prefix="/drivers", description="drivers routes")



@drivers.route("/dashboard") 
@login_required
@role_required("driver")
def dashboard():
    print(current_user)
    return render_template("driver_dashboard.html")

@drivers.route("/display_rides")
@login_required
@role_required('driver')
def display_rides():
     rides = RideOrder.query.filter_by(status='pending').all()
     return render_template('display_rides.html', rides=rides)



# Route to accept a ride
@drivers.route("/accept_ride/<int:ride_id>", methods=['GET','POST'])
@login_required  # Ensure the user is logged in
@role_required('driver')  # Ensure the user has the 'driver' role
def accept_ride(ride_id):
    """
    Allows a driver to accept a ride order.
    """
    # Retrieve the ride order by its ID. If it doesn't exist, return a 404 error.
    ride_order = RideOrder.query.get_or_404(ride_id)

    # Check if the ride has already been accepted or completed.
    if ride_order.status != 'pending':
        flash("Ride has already been accepted or completed.", 'danger')
        return redirect(url_for('drivers.display_rides')) 
    
    # Update the ride order to indicate it has been accepted by the current driver.
    ride_order.driver_id = current_user.id  
    ride_order.status = 'accepted'
    ride_order.accepted_time = datetime.utcnow()  

    # Commit the changes to the database.
    db.session.commit()

    # Flash a success message
    flash("Ride accepted successfully!", 'success')

    # Render the ride acceptance details template
    return render_template('ride_accepted.html', ride_order=ride_order)

@drivers.route("/decline_ride/<int:ride_id>", methods=['GET','POST'])
@login_required
@role_required('driver')
def decline_ride(ride_id):
    # Retrieve the ride order by its ID. If it doesn't exist, return a 404 error.
    ride_order = RideOrder.query.get_or_404(ride_id)

    # Check if the ride has already been accepted or completed.
    if ride_order.status != 'pending':
        flash("Ride has already been accepted or completed.", 'danger')
        return redirect(url_for('drivers.dashboard'))
    
    # Update the ride order to indicate it has been declined by the current driver.
    ride_order.driver_id = current_user.id
    ride_order.status = 'declined'

    # Commit the changes to the database.
    db.session.commit()

    # Flash a success message
    flash("Ride declined successfully!", 'success')

    return redirect(url_for('drivers.dashboard'))

@drivers.route("/logout")
@login_required
@role_required("driver")
def logout():
  logout_user()
  return redirect(url_for("users.user_login"))
