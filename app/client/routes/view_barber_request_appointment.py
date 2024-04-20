from flask import render_template, redirect, url_for, flash
from datetime import datetime

from ...utils.decorators import has_role
from ...queries import users, schedules
from ...utils.user import current_user
from ...utils.appointment import create_if_valid
from .. import client
from .forms.request import RequestAppointmentForm, get_service_choices


@client.route("barber/<int:barber_id>/<booked_date>", methods=["GET", "POST"])
@has_role("Client")
def barber_details_request_appointment(barber_id, booked_date):
    user = current_user()

    barbers = users.list_barbers()

    barber = users.retrieve_user(barber_id)
    booked_date = datetime.strptime(booked_date, "%Y%m%d").date()
    availability = schedules.schedule_for_date(barber_id, booked_date)

    form = RequestAppointmentForm()
    form.services.choices = get_service_choices(barber_id)
    if form.cancel.data:
        return redirect(url_for("client.view_barber", barber_id=barber_id))
    if form.validate_on_submit():
        services = form.services.data
        print(services)
        start_time = datetime.combine(datetime.min, form.start_time.data) - datetime.min
        duration = form.duration.data
        try:
            create_if_valid(
                barber=barber,
                client_id=user.id,
                start_date=booked_date,
                start_time=start_time,
                duration=duration,
                services=services
            )
            flash("Appointment requested", category="success")
            return redirect(url_for("client.client_home"))
        except AssertionError as error:
            print(error)
            flash(error, category="error")    
    return render_template(
        "client/view_barber_create_appointment.html", 
        user=user, 
        barbers=barbers,
        current_barber_id=int(barber_id),
        barber=barber,
        booked_date=booked_date,
        availability=availability,
        form=form
    )