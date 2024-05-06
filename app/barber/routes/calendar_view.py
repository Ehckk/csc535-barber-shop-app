from datetime import date, datetime, timedelta
from flask import flash, redirect, render_template, request, url_for

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


@barber.route("/calendar/<selected>", methods=["GET"])
@has_role("Barber")
def calendar_view(selected):
    user: BarberUser = current_user()

    today = date.today()
    selected = datetime.strptime(selected, DATE_FORMAT).date()
    current = request.args.get("d", default=None, type=str) or today.strftime(DATE_FORMAT)
    current = datetime.strptime(current, DATE_FORMAT).date()
    unit = Interval.MONTH
    if selected < today:
        return redirect(url_for("barber.calendar_view", selected=today, unit=unit, d=current))
    today_month = date(today.year, today.month, 1)
    if current < today_month:
        return redirect(url_for("barber.calendar", unit=Interval.MONTH, d=today))
    prev_date, next_date = date_increments(current, unit)
    
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

    template_key = "edit"
    is_unavailable = availability.has_unavailability_for_date(user.id, selected)
    return render_template(
        f"barber/{date_templates[unit].format(template_key)}", 
        title=date_names[unit](current),
        unit=unit,
        current=current,
        weekday=weekdays[current.weekday()],
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
        selected=selected,
        today=today
    )


@barber.route("/calendar/<selected>/unavailable", methods=["GET"])
@has_role("Barber")
def calendar_unavailable(selected: str):
    user = current_user()

    today = date.today()
    selected = datetime.strptime(selected, DATE_FORMAT).date()
    current = request.args.get("d", default=None, type=str) or today.strftime(DATE_FORMAT)
    current = datetime.strptime(current, DATE_FORMAT).date()
    unit = Interval.MONTH

    if availability.has_unavailability_for_date(user.id, selected):
        selected_fmt = selected.format("%B %d, %Y")
        flash(f"You are already unavailable on {selected_fmt}", category="error")
    else:
        availability.insert_unavailable_range(user.id, selected, None)
        flash("Availability updated", category="success")
    return redirect(url_for("barber.calendar_view", selected=selected, unit=unit, d=current))


@barber.route("/calendar/<selected>/available", methods=["GET"])
@has_role("Barber")
def calendar_available(selected: str):
    user = current_user()

    today = date.today()
    selected = datetime.strptime(selected, DATE_FORMAT).date()
    current = request.args.get("d", default=None, type=str) or today.strftime(DATE_FORMAT)
    current = datetime.strptime(current, DATE_FORMAT).date()
    unit = Interval.MONTH

    if not availability.has_unavailability_for_date(user.id, selected):
        selected_fmt = selected.format("%B %d, %Y")
        flash(f"You are already available on {selected_fmt}", category="error")
    else:
        availability.mark_available(user.id, selected)
        flash("Availability updated", category="success")
    return redirect(url_for("barber.calendar_view", selected=selected, unit=unit, d=current))


@barber.route("/calendar/<start>/<end>", methods=["GET"])
def calendar_range(start, end):
    user: BarberUser = current_user()

    today = date.today()
    selected = datetime.strptime(selected, DATE_FORMAT).date()
    current = request.args.get("d", default=None, type=str) or today.strftime(DATE_FORMAT)
    current = datetime.strptime(current, DATE_FORMAT).date()
    unit = request.args.get("unit", default=Interval.DAY, type=str)
    if unit not in interval_values:
        unit = Interval.DAY
    if unit == Interval.WEEK:
        if current < today - timedelta(days=today.weekday()):
            return redirect(url_for("barber.calendar", unit=Interval.WEEK, d=today))     
    elif current < today:
        return redirect(url_for("barber.calendar", unit=Interval.DAY, d=today))   

    prev_date, next_date = date_increments(current, unit)
    
    barber_schedule = schedules.barber_weekly_schedule(user.id, unit, current)
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
    is_unavailable = availability.has_unavailability_for_date(user.id, selected)
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
        selected=selected,
        today=today
    )