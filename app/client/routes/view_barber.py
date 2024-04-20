from flask import flash, redirect, render_template, url_for

from ...queries import users, services, schedules
from ...utils.user import current_user
from ...utils.table import get_services_table, get_schedule_table
from .. import client
from .forms.request import RequestDateForm


@client.route("/barber/<barber_id>", methods=["GET", "POST"])
def barber_details(barber_id):
    user = current_user()
    barbers = users.list_barbers()
    barber = users.retrieve_user(barber_id)

    barber_services = services.list_barber_services(barber.id)
    services_data = get_services_table(barber_services)

    barber_schedule = schedules.barber_weekly_schedule(barber.id)
    schedule_data = get_schedule_table(barber_schedule)

    form = RequestDateForm()
    if form.validate_on_submit():
        booked_date = form.date.data
        if schedules.is_available_for_date(barber_id, booked_date):
            return redirect(url_for(
                "client.barber_details_request_appointment", 
                barber_id=barber.id,
                booked_date=booked_date.strftime("%Y%m%d")
            ))
        message = f"{barber.display_name()} is unavailable on {booked_date}"
        flash(message, category="error")

    return render_template(
        "client/view_barber.html", 
        user=user, 
        form=form,
        barbers=barbers,
        barber=barber,
        current_barber_id=int(barber_id),
        services_data=services_data,
        schedule_data=schedule_data
    )