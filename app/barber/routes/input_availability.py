from flask import current_app, render_template, url_for, redirect, flash
from ...utils.decorators import has_role
from .forms.schedule import ScheduleForm
from ...utils.user import current_user
from .. import barber
from ...queries.schedules import create_schedule

@barber.route("/availability", methods=["GET", "POST"])
@has_role("Barber")
def schedule_availability():
    form = ScheduleForm()
    if form.validate_on_submit():
        user = current_user()
        weekday = form.weekday.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        id = user.id
        create_schedule(weekday, id, start_time, end_time)
        flash("Schedule Created")

    return render_template('barber/schedule.html', form=form)