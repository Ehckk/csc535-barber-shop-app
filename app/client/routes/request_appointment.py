from flask import flash, redirect, render_template, url_for
from datetime import datetime

from ...queries import users, appointments, schedules
from ...utils.decorators import has_role
from ...utils.user import current_user
from ...utils.appointment import create_if_valid
from .. import client
from .forms.request import RequestAppointmentForm, get_service_choices


@client.route("/<int:barber_id>/<booked_date>", methods=["GET", "POST"])
@has_role("Client")
def request_appointment(barber_id, booked_date):
    user = current_user()
    
    client_appointments = appointments.list_client_appointments(user.id)
    requested_appointments = appointments.list_client_appointments(user.id, is_booked=False)
    
    barber = users.retrieve_user(barber_id)
    booked_date = datetime.strptime(booked_date, "%Y%m%d").date()
    availability = schedules.schedule_for_date(barber_id, booked_date)
    
    form = RequestAppointmentForm()
    form.services.choices = get_service_choices(barber_id)
    if form.cancel.data:
        return redirect(url_for("client.client_home"))
    if form.validate_on_submit():
        services = form.services.data
        print(form.services.data)
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
            flash(error, category="error")
    return render_template(
        'client/create_appointment.html',
        user=user,
        form=form,
        appointments=client_appointments,
        requested_appointments=requested_appointments,
        barber=barber,
        booked_date=booked_date,
        availability=availability
    )
