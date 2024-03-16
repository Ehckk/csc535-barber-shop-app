from flask import render_template
from ...utils.user import current_user
from .. import client


@client.route("/appointments", methods=["GET"])
def appointments():
    user = current_user()
    return render_template('client/appointments.html', user=user)
