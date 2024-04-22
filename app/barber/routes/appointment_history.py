from flask import render_template
from ...utils.decorators import has_role
from ...models.appointment import Appointment
from ...utils.user import current_user
from ...queries.appointments import list_barber_history
from .. import barber



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
