from flask import render_template

from ...queries.appointments import list_barber_appointments, retrieve_appointment
from ...utils.user import current_user
from .. import barber


@barber.route("/appointment/<appt_id>", methods=["GET"])
def appointment_details(appt_id):
    user = current_user()
    appointments = list_barber_appointments(user.id)
    appointment = retrieve_appointment(appt_id)
    print(appointments)
    return render_template(
        "barber/view_appointment.html", 
        user=user,
        appointments=appointments,
        appointment=appointment
    )
