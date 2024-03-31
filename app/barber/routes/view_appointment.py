from flask import render_template
from ...queries.appointments import list_barber_appointments, retrieve_appointment
from ...utils.user import current_user
from .. import barber


@barber.route("/<int:appt_id>", methods=["GET"])
def appointment_details(appt_id):
    user = current_user()
    booked_appointments = list_barber_appointments(user.id)
    requested_appointments = list_barber_appointments(user.id, booked=False)
    appointment = retrieve_appointment(appt_id)
    return render_template(
        "barber/view_appointment.html", 
        user=user,
        booked_appointments=booked_appointments,
        requested_appointments=requested_appointments,
        appt_id=appt_id,
        appointment=appointment
    )
