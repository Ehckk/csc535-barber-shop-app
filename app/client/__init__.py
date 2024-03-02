from flask import Blueprint
from . import routes


client = Blueprint("client", __name__, url_prefix="/client")
