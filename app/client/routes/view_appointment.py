from flask import render_template

from ...queries.appointments import list_client_appointments, retrieve_appointment
from ...utils.user import current_user
from .. import client


@client.route("/appointment/<appt_id>", methods=["GET"])
def appointment_details(appt_id):
    user = current_user()
    appointments = list_client_appointments(user.id)
    appointment = retrieve_appointment(appt_id)
    return render_template(
        "client/view_appointment.html", 
        user=user,
        appointments=appointments,
        appointment=appointment
    )