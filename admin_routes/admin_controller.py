import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import render_template, flash, redirect, url_for
from forms import InvitationForm
from flask_login import  logout_user, login_required
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token


from config.models import  User, InvitationEmails, db,generate_deeplink, send_invitation_email
from decorators.decorators import role_required


admins = Blueprint("admins", "admins", url_prefix="/admins", description="admin routes")




@admins.route('/send_link', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def send_link():
    form = InvitationForm()
    if form.validate_on_submit():
        email = form.email.data
        role = form.role.data
        token = create_access_token(identity={'email': email, 'role': role})
        deeplink = generate_deeplink(email, token)
        invite_email = InvitationEmails(email=email, token=token)
        db.session.add(invite_email)
        db.session.commit()
        send_invitation_email(email, deeplink)
        flash('Invitation sent successfully!', 'success')
        return redirect(url_for('admins.dashboard'))
    return render_template('send_link.html', form=form)

@admins.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():

    # Fetch all users, drivers, and admins from the database
    users = User.query.filter_by(role='user')
    drivers = User.query.filter_by(role = 'driver')
    admins = User.query.filter_by(role = 'admin')

    # Render the admin dashboard template with the retrieved data
    return render_template('admin_dashboard.html',
                           users=users,
                           drivers=drivers,
                           admins=admins)

@admins.route("/delete-user/<int:user_id>", methods=['POST'])
@login_required
@role_required("admin")
def delete_user(user_id):
    users = User.query.get_or_404(user_id)
    db.session.delete(users)
    db.session.commit()
    flash("User deleted successfully", 'success')
    return redirect(url_for('admins.dashboard', users=users))

@admins.route("/delete-driver/<int:user_id>", methods=['POST'])
@login_required
@role_required("admin")
def delete_driver(user_id):
    drivers = User.query.get_or_404(user_id)
    db.session.delete(drivers)
    db.session.commit()
    flash("Driver deleted successfully", 'success')
    return redirect(url_for('admins.dashboard', drivers=drivers ))

@admins.route("/edit-driver/<int:user_id>", methods=['POST'])
@login_required
@role_required("admin")
def edit_driver(user_id):
    drivers = User.query.get_or_404(user_id)
    drivers.role = "user"
    db.session.add(drivers)
    db.session.commit()
    flash("Driver updated successfully", 'success')
    return redirect(url_for('admins.dashboard', drivers=drivers))

@admins.route("/edit-user/<int:user_id>", methods=['POST'])
@login_required
@role_required("admin")
def edit_user(user_id):
    users = User.query.get_or_404(user_id)
    users.role = "driver"
    db.session.add(users)
    db.session.commit()
    flash("User updated successfully", 'success')
    return redirect(url_for('admins.dashboard',  users=users))

@admins.route("/delete_admin/<int:user_id>", methods=['POST'])
@login_required
@role_required("admin")
def delete_admin(user_id):
    admins = User.query.get_or_404(user_id)
    db.session.delete(admins)
    db.session.commit()
    flash("Admin deleted successfully", 'success')
    return redirect(url_for('admins.dashboard', admins=admins ))
@admins.route("/logout")
@login_required
@role_required("admin")
def logout():
    logout_user()
    return redirect(url_for("users.user_login"))
