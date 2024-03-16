from flask import render_template
from ...utils.user import current_user
from .. import barber


@barber.route("/", methods=["GET", "POST"])
def barber_home():
    user = current_user()
    return render_template('barber/home.html', user=user)
