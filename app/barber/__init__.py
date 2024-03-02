from flask import Blueprint


barber = Blueprint("barber", __name__, url_prefix="/barber")


from .routes import *
