from datetime import date, datetime
from flask import render_template, request
from ...queries import schedules
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
from ...utils.table import get_schedule_table
from ...models.barber import BarberUser
from ...models.window import Interval
from .. import barber


@barber.route("/calendar", methods=["GET", "POST"])
@has_role("Barber")
def calendar():
    user: BarberUser = current_user()
    barber_schedule = schedules.barber_weekly_schedule(user.id)
    schedule_data = get_schedule_table(barber_schedule)

    has_availability = len(schedule_data) == 0
    
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
    title = date_names[unit](current)
    template = date_templates[unit].format("view")

    times = times_list(schedule, appointments)
    dates = dates_list(current, unit)

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
        weekdays=weekdays,
        schedule_data=schedule_data
    )
