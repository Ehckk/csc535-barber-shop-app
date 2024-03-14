from flask import render_template
from .. import client


@client.route("/barber/<barber_id>", methods=["GET"])
def barber_details(barber_id):
    return 'Barber Details'