from flask import render_template

from ...queries.appointments import list_barber_appointments
from ...utils.user import current_user
from .. import barber


@barber.route("/", methods=["GET", "POST"])
def barber_home():
    user = current_user()
    booked_appointments = list_barber_appointments(user.id)
    requested_appointments = list_barber_appointments(user.id, booked=False)
    return render_template(
        'barber/home.html', 
        user=user,
        booked_appointments=booked_appointments,
        requested_appointments=requested_appointments
    )
