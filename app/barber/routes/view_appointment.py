from flask import render_template
from .. import barber


@barber.route("/appointment/<appt_id>", methods=["GET"])
def appointment_details(appt_id):
    return 'appointment_details'
