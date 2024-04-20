from functools import wraps

from flask import flash, redirect, url_for
from . import user 

def has_role(role):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_user = user.current_user()
            if current_user.role == role:
                return func(*args, **kwargs)
            
            message = f"You do not have access to {role} functions"
            flash(message, category="error")
            return redirect(url_for("auth.logout"))
        return inner
    return decorator

def has_listed_availability():
    return