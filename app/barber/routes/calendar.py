from datetime import date, datetime, time
from flask import render_template, request

from ...utils.user import current_user
from ...utils.date import date_names, interval_values, date_templates, date_increments, times_list, week_start, month_start
from ...models.user import BarberUser
from ...models.window import Interval
from .. import barber


@barber.route("/calendar", methods=["GET", "POST"])
def calendar():
    user: BarberUser = current_user()
    unit = request.args.get("unit", default=Interval.DAY, type=str)
    if unit not in interval_values:
        unit = Interval.DAY
    current = request.args.get("d", default=None, type=str)
    print(current)
    if not current:
        current = date.today()
    else:
        current = datetime.strptime(current, "%Y-%m-%d").date()
    prev_date, next_date = date_increments(current, unit)
    
    # prev = request.args.get("prev", default=False, type=bool)

    schedule = user.get_schedule(current, unit)
    title = date_names[unit](current)

    template = date_templates[unit]
    times = times_list()
    return render_template(
        f"barber/{template}", 
        title=title,
        unit=unit,
        current=current,
        prev={"unit": unit, "d": prev_date.strftime("%Y-%m-%d") },
        next={"unit": unit, "d": next_date.strftime("%Y-%m-%d") },
        user=user, 
        schedule=schedule,
        times=times
    )
