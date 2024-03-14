from flask import render_template
from .. import barber


@barber.route("/calendar", methods=["GET", "POST"])
def calendar():
    return 'calendar.html'
