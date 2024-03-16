from flask import flash, redirect, render_template, session, url_for
from ...queries.users import check_email, check_password
from ...models.user import User
from .. import auth
from .forms.login import LoginForm


@auth.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = check_email(form.email.data)
        if not user:
            flash(f"No user found with email \"{email}\"")
        user = check_password(email, password)
        if not user:
            flash(f"Incorrect password")
        if user:
            flash("Login Successful")
            session["user"] = {
                "id":       user["user_id"],
                "email":    user["email"],
                "role":     user["role"]
            }
            if session["user"]["role"] == 'Barber':
                return redirect(url_for('barber.barber_home'))
            return redirect(url_for('client.client_home'))
            # Redirect to Client home if client
            # Redirect to Barber home if barber
    return render_template("login.html", form=form)
