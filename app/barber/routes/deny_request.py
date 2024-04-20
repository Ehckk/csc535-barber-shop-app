from flask import flash, redirect, url_for
from ...utils.decorators import has_role
from ...queries.appointments import retrieve_appointment, delete_appointment
from ...utils.user import current_user
from .. import barber


@barber.route("deny/<int:appt_id>", methods=["GET"])
@has_role("Barber")
def deny_request(appt_id):
    user = current_user()
    appointment = retrieve_appointment(appt_id)
    
    reason = None
    if not user.id == appointment.barber.id:
        reason = 'You cannot manage this request'
    else:
        if not appointment.is_approved:
            delete_appointment(appt_id)
            flash('Appointment Denied!', category="success")
            return redirect(url_for("barber.barber_home"))
        else:
            reason = 'This appointment is already booked'
    if reason:
        flash(f'{reason}!', category="error")
    return redirect(url_for("barber.appointment_details", appt_id=appt_id))
