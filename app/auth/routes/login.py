from flask import flash, render_template
from .. import auth
from .forms.login import LoginForm
from ..queries.login import login_user


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
            # Redirect to Client home if client
            # Redirect to Barber home if barber
    return render_template("login.html", form=form)
