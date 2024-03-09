from flask import flash, render_template, session
from ...queries.users import login_user
from .. import auth
from .forms.login import LoginForm


@auth.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = login_user(form.email.data, form.password.data)
        print(user)
        if not user:
            flash("Login Failed")
        if user:
            flash("Login Successful")
            session["user"] = user
            # Redirect to Client home if client
            # Redirect to Barber home if barber
    return render_template("login.html", form=form)
