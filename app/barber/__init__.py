from flask import Blueprint


barber = Blueprint(
    "barber", 
    __name__, 
    url_prefix="/barber",
    template_folder='./templates'
)


from .routes import *
