from flask import flash, redirect, url_for

from ...utils.email import send_mail
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

            message = """
                A requested appointment has been approved.

                Appointment: {appt}
            """.format(appt=str(appointment))
            send_mail(
                subject="Appointment Request Approved",
                recipients=[
                    appointment.barber.email,
                    appointment.client.email
                ],
                body=message
            )

            flash('Appointment Booked!', category="success")
            for conflicting_appointment in conflicting_appointments:
                appointments.delete_appointment(conflicting_appointment.id)
                message = """
                    A requested appointment has been declined.

                    Appointment: {appt}
                """.format(appt=str(conflicting_appointment))
                send_mail(
                    subject="Appointment Request Declined",
                    recipients=[
                        conflicting_appointment.barber.email,
                        conflicting_appointment.client.email
                    ],
                    body=message
                )
        else:
            reason = 'This appointment is already booked'
    if reason:
        flash(f'{reason}!', category="error")
    return redirect(url_for("barber.appointment_details", appt_id=appt_id))
