from flask import Blueprint
from . import routes


api = Blueprint("api", __name__, url_prefix="/api")
