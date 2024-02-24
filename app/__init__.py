from flask import Flask
from config import app_config
from data.db import Database


db = Database(app_config)

def create_app():
    print("Starting application...")
    
    app = Flask(__name__)
    app.secret_key = "dev"
    app.config.from_mapping(app_config)

    @app.route("/")
    def test():
        return "Test"

    return app
