from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash, current_app


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user == None:
                return redirect(url_for("index"))
            if current_user.is_authenticated:
                print(current_user)
                if current_user.role not in roles:
                    flash("You do not have access to this resource.", "warning")
                    return redirect(url_for(f'{current_user.role}s.dashboard'))
            return func(*args, **kwargs)
        return decorated_view
    return decorator
