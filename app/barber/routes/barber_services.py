from flask import render_template

from ...utils.user import current_user
from ...queries.services import list_barber_services
from .. import barber


@barber.route("/services", methods=["GET"])
def barber_services():
    user = current_user()
    services = list_barber_services(user.id)

    return render_template(
        "barber/services.html",
        user=user,
        services=services
    )