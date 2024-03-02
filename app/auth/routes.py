from .. import db
from . import auth


@auth.route("/")
def login():
    return "Login"


@auth.route("/register")
def register():
    return "Register"


@auth.route("/logout")
def logout():
    return "Logout"

