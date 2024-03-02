from flask import Blueprint
from . import routes


barber = Blueprint("barber", __name__, url_prefix="/barber")
