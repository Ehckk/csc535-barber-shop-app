from flask import Blueprint, render_template
from .. import client

@client.route("/appointments", methods=["GET"])
def appointments():
    return "Client Appointments"
