from flask import render_template

from ...utils.decorators import has_role
from ...queries.users import list_barbers
from ...utils.user import current_user
from .. import client


@client.route("/barbers", methods=["GET"])
@has_role("Client")
def browse_barbers():
    user = current_user()
    barbers = list_barbers()

    return render_template(
        "client/barbers.html", 
        user=user,
        barbers=barbers
    )