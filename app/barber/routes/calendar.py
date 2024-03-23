from collections import OrderedDict
from datetime import date, datetime, time
from flask import render_template, request

from ...utils.user import current_user
from ...utils.date import (
    date_names, 
    dates_list, 
    interval_values, 
    date_templates, 
    date_increments, 
    times_list, 
    date_window,
    weekdays
)
from ...models.user import BarberUser
from ...models.window import Interval
from ...models.appointment import Appointment
from ...queries.appointments import appointments_between_dates, appointments_for_date
from .. import barber


def calendar_appointments(barber_id, current_date, interval):
    if interval == Interval.DAY:
        appointment_data = appointments_for_date(barber_id, current_date)
    else:
        start, end = date_window(current_date, interval)
        appointment_data = appointments_between_dates(barber_id, start, end)
    appointments = OrderedDict()
    for appointment in appointment_data:
        if not appointments.get(appointment.booked_date, None):
            appointments[appointment.booked_date] = OrderedDict
        appointments[appointment.booked_date].append(appointment)
    return appointments


@barber.route("/calendar", methods=["GET", "POST"])
def calendar():
    user: BarberUser = current_user()
    unit = request.args.get("unit", default=Interval.DAY, type=str)
    if unit not in interval_values:
        unit = Interval.DAY
    current = request.args.get("d", default=None, type=str)
    if not current:
        current = date.today()
    else:
        current = datetime.strptime(current, "%Y-%m-%d").date()
    prev_date, next_date = date_increments(current, unit)
    
    schedule = user.get_schedule(current, unit)
    appointments = calendar_appointments(user.id, current, unit)
    print(schedule, appointments)
    title = date_names[unit](current)
    template = date_templates[unit]
    times = times_list(unit)
    dates=dates_list(current, unit)
    return render_template(
        f"barber/{template}", 
        title=title,
        unit=unit,
        current=current,
        prev={"unit": unit, "d": prev_date.strftime("%Y-%m-%d") },
        next={"unit": unit, "d": next_date.strftime("%Y-%m-%d") },
        user=user, 
        schedule=schedule,
        times=times,
        dates=dates,
        weekdays=weekdays
    )
