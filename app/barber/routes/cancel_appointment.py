from flask import flash, redirect, render_template, session, url_for
from ...queries.appointments import delete_appointment
from .. import barber

@barber.route("/cancel_appointment/<int:appt_id>", methods=["POST", "GET"])
def cancel_appointment(appt_id):
    delete_appointment(appt_id)  
    flash('Appointment canceled')
    return redirect(url_for('barber.appointments'))

