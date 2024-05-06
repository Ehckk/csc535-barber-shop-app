from flask import redirect, render_template, url_for
from ...utils.decorators import has_role
from ...utils.table import get_services_table
from ...utils.user import current_user
from ...queries.appointments import list_barber_history, retrieve_appointment
from ...queries.services import retrieve_appointment_services
from .. import barber


@barber.route("/history/<int:appt_id>", methods=["GET"])
@has_role("Barber")
def history_details(appt_id: int):
    user = current_user()
    historical_appointments = list_barber_history(user.id) 
    historical_appointment_ids = set(map(lambda appt: appt.id, historical_appointments))
    if not appt_id in historical_appointment_ids:
        return redirect(url_for("barber.appointment_details", appt_id=appt_id))
    appointment = retrieve_appointment(appointment_id=appt_id)

    appointment_services = retrieve_appointment_services(appt_id)
    services_data = get_services_table(appointment_services)

    return render_template(
        'barber/view_history.html',
        user=user,
        historical_appointments=historical_appointments,
        services_data=services_data,
        appointment=appointment,
        appt_id=appt_id
    )


@barber.route("/history", methods=["GET"])
@has_role("Barber")
def appointment_history():
    user = current_user()
    historical_appointments = list_barber_history(user.id) 

    return render_template(
        'barber/appointment_history.html',
        user=user,
        historical_appointments=historical_appointments
    )