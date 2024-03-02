from flask import Flask
from ..database import db, app_config
from . import auth
from . import api
from . import barber
from . import client

def create_app():
    print("Starting application...")
    
    app = Flask(__name__)
    app.secret_key = "dev"
    app.config.from_mapping(app_config)

    app.register_blueprint(auth.auth)
    app.register_blueprint(api.api)
    app.register_blueprint(barber.barber)
    app.register_blueprint(client.client)

    return app
