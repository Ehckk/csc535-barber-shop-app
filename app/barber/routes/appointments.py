from flask import Blueprint, render_template
from .. import barber

@barber.route("/appointments", methods=["GET"])
def appointments():
    return "Barber Appointments"
