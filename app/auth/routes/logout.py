from flask import flash, redirect
from ...utils.user import current_user
from .. import auth


@auth.route("/logout")
def logout():
    user = current_user()
    user.logout()
    flash("You have been logged out", category="success")
    return redirect("/")
