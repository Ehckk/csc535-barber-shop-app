from flask import render_template
from ...queries import appointments
from ...utils.user import current_user
from .. import barber


@barber.route("/<int:appt_id>", methods=["GET"])
def appointment_details(appt_id):
    user = current_user()

    booked_appointments = appointments.list_barber_appointments(user.id)
    requested_appointments = appointments.list_barber_appointments(user.id, booked=False)
    
    appointment = appointments.retrieve_appointment(appt_id)

    conflicting_appointments = None
    if not appointment.is_approved:
        conflicting_appointments = appointments.retrieve_conflicting(appointment)

    return render_template(
        "barber/view_appointment.html", 
        user=user,
        booked_appointments=booked_appointments,
        requested_appointments=requested_appointments,
        appt_id=appt_id,
        appointment=appointment,
        conflicting_appointments=conflicting_appointments
    )
