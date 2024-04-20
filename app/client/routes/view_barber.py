from flask import render_template

from ...queries import users, services, schedules
from ...utils.user import current_user
from ...utils.table import get_services_table, get_schedule_table
from .. import client


@client.route("/barber/<barber_id>", methods=["GET"])
def barber_details(barber_id):
    user = current_user()
    barbers = users.list_barbers()
    barber = users.retrieve_user(barber_id)

    barber_services = services.list_barber_services(barber.id)
    services_data = get_services_table(barber_services)

    barber_schedule = schedules.barber_weekly_schedule(barber.id)
    schedule_data = get_schedule_table(barber_schedule)
    # print(service_columns, services_data)


    return render_template(
        "client/view_barber.html", 
        user=user, 
        barbers=barbers,
        barber=barber,
        current_barber_id=int(barber_id),
        services_data=services_data,
        schedule_data=schedule_data
    )