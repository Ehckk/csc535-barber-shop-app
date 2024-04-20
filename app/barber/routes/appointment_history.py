from flask import render_template
from ...utils.decorators import has_role
from ...models.appointment import Appointment
from ...utils.user import current_user
from ...queries.appointments import list_barber_appointments
from .. import barber


@barber.route("/history", methods=["GET"])
@has_role("Barber")
def appointment_history():
    return "Barber Appointment History"