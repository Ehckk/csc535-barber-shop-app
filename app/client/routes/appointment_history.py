from flask import render_template
from ...utils.decorators import has_role
from ...models.appointment import Appointment
from ...utils.user import current_user
from ...queries.appointments import list_client_history
from .. import  client


@client.route("/history", methods=["GET"])
@has_role("Client")
def client_appointment_history():
    user = current_user()
    historical_appointments = list_client_history(user.id) 

    return render_template(
        'client/appointment_history.html',
        user=user,
        historical_appointments=historical_appointments
    )