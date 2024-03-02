from flask import Flask
from wtforms import HiddenField
from ..database import db, app_config
from .auth import auth 
from .barber import barber
from .client import client


def is_hidden_field(field):
    return isinstance(field, HiddenField)

def create_app():
    print("Starting application...")
    
    app = Flask(__name__)
    app.secret_key = "dev"
    app.config.from_mapping(app_config)

    app.jinja_env.globals['is_hidden_field'] = is_hidden_field

    app.register_blueprint(auth)
    app.register_blueprint(barber)
    app.register_blueprint(client)

    return app
