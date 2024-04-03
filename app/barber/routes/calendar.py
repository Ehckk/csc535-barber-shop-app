from flask import render_template
from ...utils.user import current_user
from .. import barber


@barber.route("/calendar", methods=["GET", "POST"])
def calendar():
    user = current_user()
    return render_template("barber/calendar.html", user=user)
