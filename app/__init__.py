from flask import Flask
from ..database import db, app_config
from .auth import auth 
from .barber import barber
from .client import client


def create_app():
    print("Starting application...")
    
    app = Flask(__name__)
    app.secret_key = "dev"
    app.config.from_mapping(app_config)

    app.register_blueprint(auth)
    app.register_blueprint(barber)
    app.register_blueprint(client)

    return app
