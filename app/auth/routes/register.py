from ... import db
from .. import auth
from flask import render_template
from .forms.register import Registration

@auth.route("/register")
def register():
    form = Registration()
    return render_template('register.html', form = form)