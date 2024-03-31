from flask import flash, redirect, url_for

from app.queries.appointments import retrieve_appointment
from ...utils.user import current_user
from .. import barber


@barber.route("/<int:appt_id>", methods=["GET"])
def approve_request(appt_id):
    user = current_user()
    appointment = retrieve_appointment(appt_id)
    reason = None
    if not user.id == appointment.barber.id:
        reason = 'You cannot manage this request'
    else:
        if not appointment.is_approved:
            approve_request(appt_id)
            flash('Appointment Booked!', category="success")
        else:
            reason = 'This appointment is already booked'
    if reason:
        flash(f'{reason}!', category="error")
    return redirect(url_for("barber.appointment_details", appt_id=appt_id))
