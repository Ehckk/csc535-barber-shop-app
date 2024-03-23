from collections import OrderedDict, defaultdict
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
    to_time,
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
    appointments = defaultdict(OrderedDict)

    for appointment in appointment_data:
        booked_date: str = appointment.booked_date.strftime("%Y-%m-%d")  # Key: date
        start_time = to_time(appointment.start_time)
        time_key = str(time(hour=start_time.hour, minute=(start_time.minute // 30) * 30))
        if not appointments.get(time_key, None):
            appointments[booked_date][time_key] = []
        appointments[booked_date][time_key].append(appointment)
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

    times = times_list(schedule, appointments)
    dates=dates_list(current, unit)
    return render_template(
        f"barber/{template}", 
        title=title,
        unit=unit,
        current=current.strftime("%Y-%m-%d"),
        prev={"unit": unit, "d": prev_date.strftime("%Y-%m-%d") },
        next={"unit": unit, "d": next_date.strftime("%Y-%m-%d") },
        user=user, 
        schedule=schedule,
        appointments=appointments,
        times=times,
        dates=dates,
        weekdays=weekdays
    )
