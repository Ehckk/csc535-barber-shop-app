from flask import flash, redirect, url_for, render_template

from ...utils.email import send_mail
from ...utils.date import to_time
from ...utils.decorators import has_role
from ...utils.table import get_schedule_table
from .. import client
from .forms.reschedule import RescheduleForm
from ...queries.appointments import update_appointment
from ...utils.user import current_user
from ...queries import appointments, schedules
from ...models.appointment import Appointment
from datetime import datetime


@client.route("/reschedule_appointment/<int:appt_id>", methods=["POST", "GET"])
@has_role("Client")
def reschedule_appointment(appt_id):
    user = current_user()
    form = RescheduleForm()

    client_appointments = appointments.list_client_appointments(user.id)
    requested_appointments = appointments.list_client_appointments(user.id, is_booked=False)
    appointment = appointments.retrieve_appointment(appt_id)

    barber_schedule = schedules.barber_weekly_schedule(appointment.barber.id)
    schedule_data = get_schedule_table(barber_schedule)

    if form.validate_on_submit():
        new_date = form.new_date.data
        new_time = datetime.combine(datetime.min, form.new_time.data) - datetime.min
        new_duration = form.new_duration.data
        new_start_datetime = datetime.combine(new_date, to_time(new_time))

        try:
            if new_start_datetime < datetime.now():
                raise AssertionError("Appointment must be in the future!")
            else:
                Appointment.validate_appointnment(
                    barber_name=appointment.barber.display_name(),
                    barber_id=appointment.barber.id,
                    start_date=new_date,
                    start_time=new_time,
                    duration=new_duration,
                    skip_validate_services=True
                )
                new_appointment = update_appointment(appt_id, new_date, to_time(new_time), new_duration)
                
                message = """
                    An appointment has been rescheduled.

                    Old booking: {old}
                    New booked: {new}
                """.format(old=str(appointment), new=str(new_appointment))
                send_mail(
                    subject="Appointment Rescheduled",
                    recipients=[
                        appointment.barber.email,
                        appointment.client.email
                    ],
                    body=message
                )
                flash("Appointment Rescheduled!", category="success")
                return redirect(url_for("client.client_home"))
        except AssertionError as error:
            flash(error, category="error")
    
    return render_template(
        'client/reschedule_appointment.html', 
        form=form, 
        user=user, 
        appointments=client_appointments, 
        requested_appointments=requested_appointments,
        appt_id=appt_id,
        schedule_data=schedule_data
    )