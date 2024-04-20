from flask import flash, redirect, url_for
from ...utils.decorators import has_role
from ...queries import appointments
from ...utils.user import current_user
from .. import barber


@barber.route("approve/<int:appt_id>", methods=["GET"])
@has_role("Barber")
def approve_request(appt_id):
    user = current_user()
    appointment = appointments.retrieve_appointment(appt_id)
    conflicting_appointments = appointments.retrieve_conflicting(appointment)
    reason = None
    if not user.id == appointment.barber.id:
        reason = 'You cannot manage this request'
    else:
        if not appointment.is_approved:
            appointments.approve_appointment(appt_id)
            # TODO email
            flash('Appointment Booked!', category="success")
            for conflicting_appointment in conflicting_appointments:
                appointments.delete_appointment(conflicting_appointment.id)
                # TODO email
        else:
            reason = 'This appointment is already booked'
    if reason:
        flash(f'{reason}!', category="error")
    return redirect(url_for("barber.appointment_details", appt_id=appt_id))
