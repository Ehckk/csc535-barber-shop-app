from flask import render_template


from ...utils.user import current_user
from ...queries.appointments import list_client_appointments
from .. import client


@client.route("/appointments", methods=["GET"])
def appointments():
    user = current_user()
    appointments = list_client_appointments(user.id)
    print(appointments)
    return render_template(
        'client/appointments.html', 
        user=user, 
        appointments=appointments
    )
