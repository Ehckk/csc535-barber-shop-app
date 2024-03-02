from ... import db
from .. import auth


@auth.route("/register")
def register():
    return "Register"
