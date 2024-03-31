from flask import render_template

from ...queries.appointments import list_barber_appointments
from ...utils.user import current_user
from .. import barber


@barber.route("/", methods=["GET", "POST"])
def barber_home():
    user = current_user()
    appointments = list_barber_appointments(user.id)
    print(appointments)
    return render_template(
        'barber/home.html', 
        user=user,
        appointments=appointments
    )
