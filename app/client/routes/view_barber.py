from flask import render_template

from ...queries import users, services
from ...utils.user import current_user
from ...utils.table import get_services_table
from .. import client


@client.route("/barber/<barber_id>", methods=["GET"])
def barber_details(barber_id):
    user = current_user()
    barbers = users.list_barbers()
    barber = users.retrieve_user(barber_id)

    barber_services = services.list_barber_services(barber.id)
    service_columns, services_data = get_services_table(barber_services)

    

    return render_template(
        "client/view_barber.html", 
        user=user, 
        barbers=barbers,
        barber=barber,
        current_barber_id=int(barber_id),
        service_columns=service_columns,
        services_data=services_data
    )