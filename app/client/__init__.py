from flask import Blueprint


client = Blueprint(
    "client", 
    __name__, 
    url_prefix="/client",
    template_folder='templates'
)


from .routes import *
