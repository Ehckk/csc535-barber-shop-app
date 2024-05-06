from datetime import date, datetime, timedelta
from flask import flash, redirect, render_template, request, url_for

from .forms.unavailable import UnavailableForm
from .forms.schedule import ScheduleForm
from ...queries import schedules, availability, appointments
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
    weekdays,
    to_time
)
from ...utils.table import get_schedule_table, get_unavailable_table, get_appointments_table
from ...models.barber import BarberUser
from ...models.window import Interval
from .. import barber


DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"


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
        form.start_date.render_kw = {"min": today, "max": next_date - timedelta(days=1)}
        form.end_date.render_kw = {"min": today}
        if form.validate_on_submit():
            start_date = form.start_date.data 
            end_date = form.end_date.data
            if end_date == start_date:
                end_date = None

            if end_date and start_date > end_date:
                flash("End date cannot be before start date!", category="error")
            elif end_date and availability.has_unavailability_for_range(user.id, start_date, end_date):
                flash("These dates have already been marked as unavailable!", category="error")
            elif not end_date and availability.has_unavailability_for_date(user.id, start_date):
                flash("These dates have already been marked as unavailable!", category="error")
            else:
                availability.mark_unavailable(user.id, start_date, end_date)
                flash("Availability updated!", category="success")               
    else:
        form = ScheduleForm()
        if unit == Interval.DAY:
            delattr(form, "weekday")
        if form.validate_on_submit():
            weekday_id = current.weekday() if unit == Interval.DAY else int(form.weekday.data)
            start_time = form.start_time.data
            end_time = form.end_time.data
            if not start_time < end_time:
                flash("End time must be after start time!", category="error")
            elif schedules.check_existing(weekday_id, user.id, start_time, end_time):
                flash("This availability is already set!", category="error")
            else:
                schedules.create_schedule(weekday_id, user.id, start_time, end_time)
                flash("Availability updated!", category="success")
    
    barber_schedule = schedules.barber_weekly_schedule(user.id, unit, current)
    schedule_data = get_schedule_table(barber_schedule)

    selected_appointments = appointments.appointments_for_date(user.id, current)
    appointments_data = get_appointments_table(selected_appointments)

    barber_unavailable_dates = availability.list_barber_unavailible_dates(user.id, current, unit)
    unavailable_dates_data = get_unavailable_table(barber_unavailable_dates, ranges=False)

    barber_unavailable_ranges = availability.list_barber_unavailible_ranges(user.id, current, unit)
    unavailable_ranges_data = get_unavailable_table(barber_unavailable_ranges)

    schedule = user.get_schedule(current, unit)
    barber_appointments = calendar_appointments(user.id, current, unit)
    unavailable = get_unavailable(barber_unavailable_dates, barber_unavailable_ranges)

    times = times_list(schedule, barber_appointments)
    dates = dates_list(current, unit)

    template_key = "view"
    is_unavailable = availability.has_unavailability_for_date(user.id, current)
    return render_template(
        f"barber/{date_templates[unit].format(template_key)}", 
        title=date_names[unit](current),
        unit=unit,
        current=current,
        is_unavailable=is_unavailable,
        weekday=weekdays[current.weekday()],
        prev={"unit": unit, "d": prev_date},
        next={"unit": unit, "d": next_date},
        user=user, 
        schedule=schedule,
        appointments=barber_appointments,
        unavailable=unavailable,
        times=times,
        dates=dates,
        weekdays=weekdays,
        schedule_data=schedule_data,
        appointments_data=appointments_data,
        unavailable_dates_data=unavailable_dates_data,
        unavailable_ranges_data=unavailable_ranges_data,
        form=form,
        today=today
    )

@barber.route("/calendar/<start>", methods=["GET", "POST"])
def calendar_window(start: str):
    user: BarberUser = current_user()

    today = date.today()
    target_time = datetime.strptime(start, TIME_FORMAT).time()
    current = request.args.get("d", default=None, type=str) or today.strftime(DATE_FORMAT)
    current = datetime.strptime(current, DATE_FORMAT).date()
    unit = request.args.get("unit", default=Interval.DAY, type=str)
    if unit not in interval_values - {Interval.MONTH}:
        unit = Interval.DAY
    prev_date, next_date = date_increments(current, unit)
    windows = schedules.barber_daily_schedule_for_time(user.id, current, target_time)
    print(windows)
    if len(windows) == 0:
        url_name = "barber.calendar"
        return redirect(url_for(url_name, unit=unit, d=current))
    current_window = windows[0]
    start_time = to_time(current_window["start_time"])
    end_time = to_time(current_window["end_time"])
    weekday_id = current_window["weekday_id"]
    
    form = ScheduleForm()
    delattr(form, "weekday")
    if form.validate_on_submit():
        weekday_id = current.weekday()
        new_start_time = form.start_time.data
        new_end_time = form.end_time.data
        if not new_start_time < new_end_time:
            flash("End time must be after start time!", category="error")
        elif schedules.check_existing(weekday_id, user.id, new_start_time, new_end_time):
            flash("This availability is already set!", category="error")
        else:
            schedules.create_schedule(weekday_id, user.id, new_start_time, new_end_time)
            # Cancel appointments outside range
            flash("Availability updated!", category="success")
            url_name = "barber.calendar_window"
            url = url_for(url_name, d=current, unit=unit, start=new_start_time)
            return redirect(url)
    form.start_time.data = start_time
    form.end_time.data = end_time

    barber_schedule = schedules.barber_weekly_schedule(user.id, Interval.DAY, current, target_time)
    print(barber_schedule)
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
    template_key = "edit"
    is_unavailable = availability.has_unavailability_for_date(user.id, current)
    return render_template(
        f"barber/{date_templates[unit].format(template_key)}", 
        title=date_names[unit](current),
        unit=unit,
        current=current,
        prev={"unit": unit, "d": prev_date},
        next={"unit": unit, "d": next_date},
        user=user, 
        schedule=schedule,
        appointments=appointments,
        unavailable=unavailable,
        is_unavailable=is_unavailable,
        times=times,
        dates=dates,
        weekdays=weekdays,
        schedule_data=schedule_data,
        unavailable_dates_data=unavailable_dates_data,
        unavailable_ranges_data=unavailable_ranges_data,
        weekday_id=weekday_id,
        start_time=start_time,
        end_time=end_time,
        today=today,
        form=form
    )