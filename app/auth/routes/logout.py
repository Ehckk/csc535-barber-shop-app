from ... import db
from .. import auth


@auth.route("/logout")
def logout():
    return "Logout"

