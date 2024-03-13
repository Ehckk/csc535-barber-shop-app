from ... import db
from .. import auth
from flask import render_template, session, render_template, redirect, url_for
from .forms.register import Registration
from ...queries import users
import sys

@auth.route("/register", methods=["GET","POST"])
def register():
    form = Registration()
    if form.validate_on_submit():
        user = dict()
        firstName = form.first_name.data
        lastName = form.last_name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        users.create_user(email,password,firstName,lastName,role)
        temp = users.check_email(form.email.data)
        print(temp)
        user["user_id"] = temp.get('user_id')
        user["email"] = form.email.data
        user["role"] = form.role.data
        session["user"] = {
        "id":       user["user_id"],
        "email":    user["email"],
        "role":     user["role"]
        }
        if session["user"]["role"] == 'Barber':
            return redirect(url_for('barber.barber_home'))
        return redirect(url_for('client.client_home'))
    return render_template('register.html', form = form)