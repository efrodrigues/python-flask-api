from flask import Flask

from .configs.api_config import api_config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    api_config(app)
    return app
