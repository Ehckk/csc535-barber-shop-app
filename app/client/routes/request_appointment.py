from flask import flash, redirect, render_template, url_for
from datetime import datetime
from ...models.appointment import Appointment 
from ...queries import users, services, appointments, schedules
from ...utils.user import current_user
from ...utils.calendar import validate_appointment_time
from ...utils.date import to_time
from .. import client
from .forms.request import RequestAppointmentForm


def get_service_choices(barber_id: int):
    barber_services = services.list_barber_services(barber_id)
    choices = list(map(
        lambda service: (service.id, str(service)), 
        barber_services
    ))
    return choices


@client.route("/<int:barber_id>/<booked_date>", methods=["GET", "POST"])
def request_appointment(barber_id, booked_date):
    user = current_user()
    barber = users.retrieve_user(barber_id)
    booked_date = datetime.strptime(booked_date, "%Y%m%d").date()
    availability = schedules.schedule_for_date(barber_id, booked_date)
    
    form = RequestAppointmentForm()
    form.services.choices = get_service_choices(barber_id)
    if form.cancel.data:
        return redirect(url_for("client.client_home"))
    if form.validate_on_submit():
        services = form.services.data
        start_time = datetime.combine(datetime.min, form.start_time.data) - datetime.min
        duration = form.duration.data
        print(services)
        if len(services) == 0:
            flash("Select at least one service!", category="error")
        else:
            if not validate_appointment_time(availability, start_time, duration):
                flash(f"{barber.display_name()} is unavailable during this time", category="error")
            else:
                appointments.create_appointment(
                    barber_id=barber.id,
                    client_id=user.id,
                    start_date=booked_date,
                    start_time=to_time(start_time),
                    duration=duration
                )
                # TODO appointment services
                flash("Appointment requested", category="success")
                return redirect(url_for("client.client_home"))
    print(availability)
    return render_template(
        'client/create_appointment.html',
        user=user,
        form=form,
        barber=barber,
        booked_date=booked_date,
        availability=availability
    )
