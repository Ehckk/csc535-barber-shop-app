from flask import render_template

from ...utils.decorators import has_role
from ...queries.appointments import list_barber_appointments
from ...utils.user import current_user
from .. import barber


@barber.route("/", methods=["GET", "POST"])
@has_role("Barber")
def barber_home():
    user = current_user()
    booked_appointments = list_barber_appointments(user.id)
    requested_appointments = list_barber_appointments(user.id, booked=False)
    return render_template(
        'barber/appointments.html', 
        user=user,
        booked_appointments=booked_appointments,
        requested_appointments=requested_appointments
    )
