from flask import render_template


from ...models.appointment import Appointment
from ...utils.user import current_user
from ...queries.appointments import list_barber_appointments
from .. import barber


@barber.route("/services", methods=["GET"])
def barber_services():
    return "Barber Services"