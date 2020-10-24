from flask import Flask
from flask_smorest import Api
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        super().__init__(map)
        self.map = map
        self.regex = args[0]


def register_routes(app: Flask, routes: list):
    api = Api(app)
    for blp in routes:
        api.register_blueprint(blp)


def routes_config(app: Flask):
    app.url_map.converters["regex"] = RegexConverter

    # XXX Informe aqui as rotas que são "importadas"
    from ..rests.health_rest import api as health_api
    from ..rests.offset_control_rest import api as offset_control_api

    routes = [
        offset_control_api,
        health_api,
    ]
    register_routes(app, routes)


def routes_config_health(app: Flask) -> None:
    # XXX Informe aqui as rotas que são "importadas"
    from ..rests.health_rest import api

    register_routes(app, [api])
