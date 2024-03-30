from datetime import date
from flask import Flask
from wtforms import HiddenField, SubmitField
from ..database import db, app_config
from .auth import auth 
from .barber import barber
from .client import client


def is_hidden_field(field):
    return isinstance(field, HiddenField)

def is_submit_field(field):
    return isinstance(field, SubmitField)

def format_date(value: date):
    return value.strftime("%Y-%m-%d") 

def create_app():
    print("Starting application...")
    
    app = Flask(__name__)
    app.secret_key = "dev"
    app.config.from_mapping(app_config)

    app.jinja_env.globals['is_hidden_field'] = is_hidden_field
    app.jinja_env.globals['is_submit_field'] = is_submit_field
    app.jinja_env.filters['format_date'] = format_date

    app.register_blueprint(auth)
    app.register_blueprint(barber)
    app.register_blueprint(client)
    return app
