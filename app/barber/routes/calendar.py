from datetime import date, datetime, timedelta
from flask import flash, redirect, render_template, request, url_for

from .forms.unavailable import UnavailableForm
from .forms.schedule import ScheduleForm
from ...queries import schedules, availability
from ...utils.decorators import has_role
from ...utils.user import current_user
from ...utils.calendar import calendar_appointments, get_unavailable
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

    today = date.today()
    current = request.args.get("d", default=None, type=str) or today.strftime(DATE_FORMAT)
    current = datetime.strptime(current, DATE_FORMAT).date()
    unit = request.args.get("unit", default=Interval.DAY, type=str)
    if unit not in interval_values:
        unit = Interval.DAY
    if unit == Interval.MONTH:
        today_month = date(today.year, today.month, 1)
        if current < today_month:
            return redirect(url_for("barber.calendar", unit=Interval.MONTH, d=today))
    elif unit == Interval.WEEK:
        if current < today - timedelta(days=today.weekday()):
            return redirect(url_for("barber.calendar", unit=Interval.WEEK, d=today))     
    elif current < today:
        return redirect(url_for("barber.calendar", unit=Interval.DAY, d=today))     
        
    prev_date, next_date = date_increments(current, unit)

    if unit == Interval.MONTH:
        form = UnavailableForm()
        date_field_kw = {"min": current, "max": next_date - timedelta(days=1)}
        form.start_date.render_kw = date_field_kw
        form.end_date.render_kw = date_field_kw
        if form.validate_on_submit():
            if form.start_date.data > form.end_date.data:
                flash("End date cannot be before start date!", category="error")
            else:
                availability.update_availability(weekday_id, user.id, start_time, end_time)
                flash("Unavailable days updated!", category="success")               
    else:
        form = ScheduleForm()
        if form.validate_on_submit():
            weekday_id = int(form.weekday.data)
            start_time = form.start_time.data
            end_time = form.end_time.data
            if not start_time < end_time:
                flash("End time must be after start time!", category="error")
            elif schedules.check_existing(weekday_id, user.id, start_time, end_time):
                flash("This availability is already set!", category="error")
            else:
                schedules.create_schedule(weekday_id, user.id, start_time, end_time)
                flash("Availability updated!", category="success")
    
    barber_schedule = schedules.barber_weekly_schedule(user.id)
    schedule_data = get_schedule_table(barber_schedule)

    barber_unavailable_dates = availability.list_barber_unavailible_dates(user.id, current, unit)
    unavailable_dates_data = get_unavailable_table(barber_unavailable_dates, ranges=False)

    barber_unavailable_ranges = availability.list_barber_unavailible_ranges(user.id, current, unit)
    unavailable_ranges_data = get_unavailable_table(barber_unavailable_ranges)

    schedule = user.get_schedule(current, unit)
    appointments = calendar_appointments(user.id, current, unit)
    unavailable = get_unavailable(barber_unavailable_dates, barber_unavailable_ranges)

    times = times_list(schedule, appointments)
    dates = dates_list(current, unit)

    template_key = "view"
    print(unavailable)
    return render_template(
        f"barber/{date_templates[unit].format(template_key)}", 
        title=date_names[unit](current),
        unit=unit,
        current=current.strftime("%Y-%m-%d"),
        prev={"unit": unit, "d": prev_date},
        next={"unit": unit, "d": next_date},
        user=user, 
        schedule=schedule,
        appointments=appointments,
        unavailable=unavailable,
        times=times,
        dates=dates,
        weekdays=weekdays,
        schedule_data=schedule_data,
        unavailable_dates_data=unavailable_dates_data,
        unavailable_ranges_data=unavailable_ranges_data,
        form=form,
        today=today
    )
