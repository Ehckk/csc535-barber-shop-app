from flask import Flask, request, render_template, redirect, url_for, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash

from .. import auth
from .forms.request_reset import RequestResetForm
from .forms.reset_password import ResetPasswordForm
from ...queries.find_user_by_email import find_user_by_email
from ...queries.update_user_password import update_user_password
from ...utils.send_password_reset_email import send_password_reset_email


@auth.route("/request_reset", methods=["GET", "POST"])
def request_reset():
    form = RequestResetForm()    
    if form.validate_on_submit():
        email = form.email.data
        user = find_user_by_email(email)
        if user:
            serializer = URLSafeTimedSerializer("dev")
            token = serializer.dumps(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            send_password_reset_email(email, reset_url)
            flash('Check your email to reset your password', category="success")
        else:
            flash('Email does not match any user', category="error")
    return render_template('request_reset.html', form=form)


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()
    serializer = URLSafeTimedSerializer("dev")
    try:
        email = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        flash("Invalid Token", category="error")
        return redirect(url_for("auth.login")) 
    if form.validate_on_submit():
        new_password = form.password.data
        new_confirm_password = form.confirm_password.data
        if not new_confirm_password == new_password:
            flash("Passwords do not match", category="error")
        else: 
            update_user_password(email, new_password)
            flash('Your password has been updated', category="success")
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, token=token)