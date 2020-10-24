from flask import Flask
from flask_marshmallow import Marshmallow
from maaslogger.base_logger import get_logger

from ..utils import settings
from .cache_config import cache_config
from .cors_config import cors_config
from .db_config import db_config
from .error_handler_config import app_errorhandling_config

# from .interceptors_config import interceptors_config
from .openapi_config import openapi_config
from .routes_config import routes_config, routes_config_health

logger = get_logger(__name__)


def api_config(app: Flask) -> None:
    logger.debug("Configurando a API flask.")

    # TODO: implementar caso seja necessario interceptor
    # interceptors_config(app)

    # app.secret_key = settings.get_secret_key()
    # XXX Terá upload seu projeto?
    app.config["MAX_CONTENT_LENGTH"] = settings.getenv_int(
        "MAX_CONTENT_LENGTH_BYTES", 10 * 1024 * 1024
    )

    openapi_config(app)
    cors_config(app)
    Marshmallow(app)
    routes_config(app)
    app_errorhandling_config(app)
    cache_config(app)
    db_config(app)


def init_worker_api(name: str) -> Flask:
    app = Flask(name)
    # TODO: implementar caso seja necessario interceptor
    # interceptors_config(app)
    openapi_config(app)
    routes_config_health(app)
    app_errorhandling_config(app)
    db_config(app)
    return app
