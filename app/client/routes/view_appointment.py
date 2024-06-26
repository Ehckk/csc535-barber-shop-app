from flask import render_template

from ...utils.decorators import has_role
from ...utils.table import get_services_table
from ...queries import appointments, services
from ...utils.user import current_user
from .. import client


@client.route("/<int:appt_id>", methods=["GET"])
@has_role("Client")
def appointment_details(appt_id):
    user = current_user()
    client_appointments = appointments.list_client_appointments(user.id)
    requested_appointments = appointments.list_client_appointments(user.id, is_booked=False)

    appointment = appointments.retrieve_appointment(appt_id)
    appointment_services = services.retrieve_appointment_services(appt_id)
    services_data = get_services_table(appointment_services)

    return render_template(
        "client/view_appointment.html", 
        user=user,
        appointments=client_appointments,
        requested_appointments=requested_appointments,
        appointment=appointment,
        appt_id=appt_id,
        services_data=services_data
    )