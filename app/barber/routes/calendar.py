from datetime import date, datetime, timedelta
from flask import flash, render_template, request

from .forms.unavailable import UnavailableForm
from .forms.schedule import ScheduleForm
from ...queries import schedules, availability
from ...utils.decorators import has_role
from ...utils.user import current_user
from ...utils.calendar import calendar_appointments
from ...utils.date import (
    date_names, 
    dates_list, 
    interval_values, 
    date_templates, 
    date_increments, 
    times_list, 
    weekdays
)
from ...utils.table import get_schedule_table, get_unavailable_table
from ...models.barber import BarberUser
from ...models.window import Interval
from .. import barber

DATE_FORMAT = "%Y-%m-%d"


@barber.route("/calendar", methods=["GET", "POST"])
@has_role("Barber")
def calendar():
    user: BarberUser = current_user()

    today = date.today().strftime(DATE_FORMAT)
    current = request.args.get("d", default=None, type=str) or today
    current = datetime.strptime(current, DATE_FORMAT).date()

    unit = request.args.get("unit", default=Interval.DAY, type=str)
    if unit not in interval_values:
        unit = Interval.DAY
    prev_date, next_date = date_increments(current, unit)

    if unit == Interval.MONTH:
        form = UnavailableForm()
        date_field_kw = {"min": current, "max": next_date - timedelta(days=1)}
        form.start_date.render_kw = date_field_kw
        form.end_date.render_kw = date_field_kw
        if form.validate_on_submit():
            if form.start_date.data > form.end_date.data:
                flash("End date cannot be before start date!", category="error")
                # 
    else:
        form = ScheduleForm()
        # if form.validate_on_submit():
    
    barber_schedule = schedules.barber_weekly_schedule(user.id)
    schedule_data = get_schedule_table(barber_schedule)

    barber_unavailable_dates = availability.list_barber_unavailible_dates(user.id, current, unit)
    unavailable_dates_data = get_unavailable_table(barber_unavailable_dates, ranges=False)

    barber_unavailable_ranges = availability.list_barber_unavailible_ranges(user.id, current, unit)
    unavailable_ranges_data = get_unavailable_table(barber_unavailable_ranges)

    schedule = user.get_schedule(current, unit)
    appointments = calendar_appointments(user.id, current, unit)
    times = times_list(schedule, appointments)
    dates = dates_list(current, unit)

    template_key = "view"
    return render_template(
        f"barber/{date_templates[unit].format(template_key)}", 
        title=date_names[unit](current),
        unit=unit,
        current=current.strftime("%Y-%m-%d"),
        prev={"unit": unit, "d": prev_date.strftime("%Y-%m-%d") },
        next={"unit": unit, "d": next_date.strftime("%Y-%m-%d") },
        user=user, 
        schedule=schedule,
        appointments=appointments,
        times=times,
        dates=dates,
        weekdays=weekdays,
        schedule_data=schedule_data,
        unavailable_dates_data=unavailable_dates_data,
        unavailable_ranges_data=unavailable_ranges_data,
        form=form
    )
