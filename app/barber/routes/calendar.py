from datetime import date
from flask import render_template, request
from collections import defaultdict

from ...utils.user import current_user
from ...models.user import BarberUser
from ...models.window import Interval
from .. import barber


@barber.route("/calendar", methods=["GET", "POST"])
def calendar():
    user: BarberUser = current_user()
    unit = request.args.get("unit", default=0, type=int)
    value = request.args.get("value", default=Interval.DAY, type=str)
    is_prev = request.args.get("prev", default=False, type=bool)


    user.get_schedule()
    return render_template(
        "barber/calendar.html", 
        user=user, 
        title=
    )
