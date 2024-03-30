from flask import render_template

from ...queries.users import retrieve_user
from ...utils.email import send_verification_email
from .. import auth

@auth.route("/verify/<user_id>", methods=["GET"])
def verify(user_id):
    user = retrieve_user(int(user_id))
    send_verification_email(user.id, user.email)
    return render_template("verify.html", email=user.email)
