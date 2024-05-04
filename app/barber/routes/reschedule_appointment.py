from flask import flash, redirect, url_for, render_template
from ...utils.decorators import has_role
from .. import barber
from .forms.reschedule import RescheduleForm
from ...queries.appointments import update_appointment
from ...utils.user import current_user
from ...queries import appointments

@barber.route("/reschedule_appointment/<int:appt_id>", methods=["POST", "GET"])
@has_role("Barber")
def reschedule_appointment(appt_id):
    user = current_user()
    form = RescheduleForm()

    barber_appointments = appointments.list_barber_appointments(user.id)
    requested_appointments = appointments.list_barber_appointments(user.id, booked=False)

    if form.validate_on_submit():
        new_date = form.new_date.data
        new_time = form.new_time.data
        new_duration = form.new_duration.data
        update_appointment(appt_id,new_date, new_time, new_duration)
        flash("Appointment Edited!")
        return redirect(url_for("barber.barber_home"))
    return render_template('barber/reschedule_appointment.html', form = form, user = user, barber_appointments = barber_appointments, requested_appointments = requested_appointments)