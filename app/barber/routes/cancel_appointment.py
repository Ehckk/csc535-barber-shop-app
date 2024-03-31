from flask import flash, redirect, url_for
from ...queries.appointments import delete_appointment
from .. import barber


@barber.route("/cancel/<int:appt_id>", methods=["POST", "GET"])
def cancel_appointment(appt_id):
    delete_appointment(appt_id)  
    flash('Appointment canceled', category="success")
    return redirect(url_for('barber.home'))
