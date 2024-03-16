from flask import render_template


from ...models.appointment import Appointment
from ...utils.user import current_user
from ...queries.appointments import list_barber_appointments
from .. import barber


@barber.route("/appointments", methods=["GET"])
def appointments():
    user = current_user()
    appointments = list_barber_appointments(user.id)
    print(appointments)
    return render_template(
        'barber/appointments.html', 
        user=user, 
        appointments=appointments
    )