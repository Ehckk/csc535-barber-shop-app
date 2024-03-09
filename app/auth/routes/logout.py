from flask import redirect
from ...utils.user import current_user
from .. import auth


@auth.route("/logout")
def logout():
    user = current_user()
    user.logout()
    return redirect("/")
