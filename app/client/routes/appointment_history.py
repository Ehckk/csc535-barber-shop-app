from flask import redirect, render_template, url_for

from ...utils.table import get_services_table
from ...utils.decorators import has_role
from ...utils.user import current_user
from ...queries.appointments import list_client_history, retrieve_appointment
from ...queries.services import retrieve_appointment_services
from .. import  client


@client.route("/history/<int:appt_id>", methods=["GET"])
@has_role("Client")
def history_details(appt_id: int):
    user = current_user()
    historical_appointments = list_client_history(user.id) 
    historical_appointment_ids = set(map(lambda appt: appt.id, historical_appointments))
    if not appt_id in historical_appointment_ids:
        return redirect(url_for("client.appointment_details", appt_id=appt_id))
    appointment = retrieve_appointment(appointment_id=appt_id)

    appointment_services = retrieve_appointment_services(appt_id)
    services_data = get_services_table(appointment_services)

    return render_template(
        'client/view_history.html',
        user=user,
        historical_appointments=historical_appointments,
        services_data=services_data,
        appointment=appointment,
        appt_id=appt_id
    )


@client.route("/history", methods=["GET"])
@has_role("Client")
def client_appointment_history():
    user = current_user()
    historical_appointments = list_client_history(user.id) 

    return render_template(
        'client/appointment_history.html',
        user=user,
        historical_appointments=historical_appointments
    )