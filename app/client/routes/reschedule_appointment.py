from flask import flash, redirect, url_for, render_template
from ...utils.decorators import has_role
from .. import client
from .forms.reschedule import RescheduleForm
from ...queries.appointments import update_appointment
from ...utils.user import current_user
from ....app.queries import appointments

@client.route("/reschedule_appointment/<int:appt_id>", methods=["POST", "GET"])
@has_role("Client")
def reschedule_appointment(appt_id):
    user = current_user()
    form = RescheduleForm()

    client_appointments = appointments.list_client_appointments(user.id)
    requested_appointments = appointments.list_client_appointments(user.id, is_booked=False)

    if form.validate_on_submit():
        new_date = form.new_date.data
        new_time = form.new_time.data
        new_duration = form.new_duration.data
        update_appointment(appt_id,new_date, new_time, new_duration)
        flash("Appointment Edited!")
        return redirect(url_for("client.client_home"))
    return render_template('client/reschedule_appointment.html', form = form, user = user, client_appointments = client_appointments, requested_appointments = requested_appointments)