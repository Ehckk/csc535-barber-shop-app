from flask import render_template
from .. import client


@client.route("/barbers", methods=["GET"])
def browse_barbers():
    return 'Browse Barbers'