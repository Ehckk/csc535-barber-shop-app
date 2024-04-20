from flask import flash, redirect, url_for
from ...utils.decorators import has_role
from ...queries.appointments import delete_appointment
from .. import client

@client.route("/cancel_appointment/<int:appt_id>", methods=["POST", "GET"])
@has_role("Client")
def cancel_appointment(appt_id):
    delete_appointment(appt_id)  
    flash('Appointment canceled', category="error")
    return redirect(url_for('client.client_home'))