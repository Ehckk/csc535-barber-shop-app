from flask import Blueprint


auth = Blueprint(
    "auth", 
    __name__, 
    url_prefix="/",
    template_folder='templates'
)


from .routes import *
