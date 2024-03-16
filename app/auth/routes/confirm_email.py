from .. import auth
from flask import current_app, url_for, redirect, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

@auth.route("/confirm_email/<token>")
def confirm_email(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        s.loads(token, max_age=60)
    except SignatureExpired:
        flash('Invaild Token')
        return redirect(url_for('auth.login'))
    return True