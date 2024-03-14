from flask import render_template
from .. import client


@client.route("/appointment/<appt_id>", methods=["GET"])
def appointment_details(appt_id):
    return 'Client Appointment Details'