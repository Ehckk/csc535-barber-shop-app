from flask import render_template


from ...models.appointment import Appointment
from ...utils.user import current_user
from ...queries.appointments import list_client_appointments
from .. import client


@client.route("/appointments", methods=["GET"])
def appointments():
    user = current_user()
    appointments = [] 
    for appointment_data in list_client_appointments(user.id):
        appointment = Appointment(**appointment_data)
        appointments.append(appointment)
    print(appointments)
    return render_template('client/appointments.html', user=user, appointments=appointments)
