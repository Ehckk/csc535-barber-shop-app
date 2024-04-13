from flask import render_template

from ...queries.users import list_barbers, retrieve_user
from ...utils.user import current_user
from .. import client


@client.route("/barber/<barber_id>", methods=["GET"])
def barber_details(barber_id):
    user = current_user()
    barbers = list_barbers()
    barber = retrieve_user(barber_id)
    
    return render_template(
        "client/view_barber.html", 
        user=user, 
        barbers=barbers,
        barber=barber
    )