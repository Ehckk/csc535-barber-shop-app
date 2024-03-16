from flask import render_template
from ...utils.user import current_user
from .. import client


@client.route("/barbers", methods=["GET"])
def browse_barbers():
    user = current_user()
    return render_template("client/barbers.html", user=user)