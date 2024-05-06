from flask import flash, redirect, url_for
from ...utils.decorators import has_role
from ...utils.email import send_mail
from ...queries.appointments import delete_appointment, retrieve_appointment
from .. import client


@client.route("/cancel_appointment/<int:appt_id>", methods=["POST", "GET"])
@has_role("Client")
def cancel_appointment(appt_id):
    appointment = retrieve_appointment(appt_id)
    delete_appointment(appt_id)  

    message = """
        An appointment has been canceled.

        Appointment: {appt}
    """.format(appt=str(appointment))
    send_mail(
        subject="Appointment Canceled",
        recipients=[
            appointment.barber.email,
            appointment.client.email
        ],
        body=message
    )

    flash('Appointment canceled', category="success")
    return redirect(url_for('client.client_home'))