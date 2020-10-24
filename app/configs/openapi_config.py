from importlib import resources

from flask import Flask

from ..utils.settings import get_app_version, getenv


def openapi_config(app: Flask) -> None:
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["API_VERSION"] = get_app_version()

    app.config["OPENAPI_JSON_PATH"] = getenv("OPENAPI_JSON_PATH")
    app.config["OPENAPI_URL_PREFIX"] = getenv("OPENAPI_URL_PREFIX")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = getenv("OPENAPI_SWAGGER_UI_PATH")
    app.config["OPENAPI_SWAGGER_UI_URL"] = getenv("OPENAPI_SWAGGER_UI_URL")
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = getenv(
        "OPENAPI_SWAGGER_UI_VERSION"
    )
    app.config["OPENAPI_REDOC_PATH"] = getenv("OPENAPI_REDOC_PATH")
    app.config["OPENAPI_REDOC_URL"] = getenv("OPENAPI_REDOC_URL")

    description_md = resources.read_text(__package__, "openapi_description.md")
    openapi_info = {"title": "MaaS Integra API", "description": description_md}
    app.config["API_TITLE"] = "MaasIntegraApi"
    app.config["API_SPEC_OPTIONS"] = {
        "info": openapi_info,
        "security": [{"bearerAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Token JWT",
                },
            }
        },
    }
