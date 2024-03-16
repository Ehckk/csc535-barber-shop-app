from flask import Blueprint, render_template
from .. import barber

@barber.route("/requests", methods=["GET"])
def appointments_requests():
    return "Barber Appointment Requests"