from flask import render_template
from ...utils.user import current_user
from .. import barber


@barber.route("/appointment/<appt_id>", methods=["GET"])
def appointment_details(appt_id):
    user = current_user()
    return render_template("calendar.html", user=user)
