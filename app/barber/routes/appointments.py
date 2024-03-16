from flask import render_template
from ...utils.user import current_user
from .. import barber


@barber.route("/appointments", methods=["GET"])
def appointments():
    user = current_user()
    return render_template('barber/appointments.html', user=user)
