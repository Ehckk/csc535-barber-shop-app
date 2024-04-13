from flask import render_template


from ...utils.user import current_user
from ...queries.appointments import list_client_appointments
from .. import client


@client.route("/history", methods=["GET"])
def appointment_history():
    return "client Appointment History"