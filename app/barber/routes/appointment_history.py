from flask import render_template


from ...models.appointment import Appointment
from ...utils.user import current_user
from ...queries.appointments import list_barber_appointments
from .. import barber


@barber.route("/history", methods=["GET"])
def appointment_history():
    return "Barber Appointment History"