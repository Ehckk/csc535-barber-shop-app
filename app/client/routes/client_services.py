from flask import render_template


from ...utils.user import current_user
from ...queries.appointments import list_client_appointments
from .. import client


@client.route("/services", methods=["GET"])
def client_services():
    return "Client Services"