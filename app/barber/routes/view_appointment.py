from flask import redirect, render_template, url_for
from ...utils.decorators import has_role
from ...queries import appointments, services
from ...utils.user import current_user
from ...utils.table import get_services_table
from .. import barber


@barber.route("/<int:appt_id>", methods=["GET"])
@has_role("Barber")
def appointment_details(appt_id):
    user = current_user()

    booked_appointments = appointments.list_barber_appointments(user.id)
    requested_appointments = appointments.list_barber_appointments(user.id, booked=False)
    appointment_ids = set(map(lambda appt: appt.id, booked_appointments + requested_appointments))
    if not appt_id in appointment_ids:
        return redirect(url_for("barber.history_details", appt_id=appt_id))
    appointment = appointments.retrieve_appointment(appt_id)
    appointment_services = services.retrieve_appointment_services(appt_id)
    services_data = get_services_table(appointment_services)

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
        conflicting_appointments=conflicting_appointments,
        services_data=services_data
    )
