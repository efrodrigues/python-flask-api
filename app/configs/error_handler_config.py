from dataclasses import asdict, dataclass
from uuid import uuid4

from flask import Flask, jsonify
from maaslogger.base_logger import get_logger
from werkzeug.exceptions import HTTPException, UnprocessableEntity

from ..utils.exceptions import AppErrorCode, ApplicationException

logger = get_logger(__name__)


@dataclass
class ErrorResponse:
    code: int = None
    message: str = None
    details: any = None

    def as_dict(self):
        return asdict(self)

    @classmethod
    def build_dict(
        cls, app_error_code: int, description: str, details: any = None
    ) -> dict:
        error_msg = cls(
            code=app_error_code, message=description, details=details
        )
        return error_msg.as_dict()


def _serialize_error(
    http_error_code: int,
    app_error_code: int,
    message: str,
    details: any = None,
) -> tuple:
    error_message = ErrorResponse.build_dict(app_error_code, message, details)
    return jsonify(error_message), http_error_code


def _serialize_app_error(
    http_error_code: int, app_error: AppErrorCode, details: any = None
):
    return _serialize_error(
        http_error_code,
        app_error.value.code,
        app_error.value.description,
        details,
    )


# XXX Faça isto em outro lugar!
def _translate(msg: str) -> str:
    str_browser_not_understand = (
        "The browser (or proxy) sent a request that this "
        "server could not understand."
    )
    what = {
        "Field is required": "Campo é obrigatório.",
        str_browser_not_understand: "Enviada uma requisição não entendida.",
    }
    return what.get(msg, msg)


def app_errorhandling_config(app: Flask):
    # TODO: ajustar erro de unicidade
    # @app.errorhandler(mongoengine.NotUniqueError)
    # def handle_not_unique_error(e):
    #     # XXX Rever
    #     return _serialize_app_error(
    #         400, AppErrorCode.ERROR_DB_NOT_UNIQUE, details=str(e),
    #     )

    # TODO: ajustar erro de validacao
    # @app.errorhandler(mongoengine.ValidationError)
    # def handle_validation_error(e):
    #     if isinstance(e.errors, dict):
    #         details = {
    #             k: _translate(v.message) if v.message else str(v)
    #             for k, v in e.errors.items()
    #         }
    #     else:
    #         details = str(e)
    #     return _serialize_app_error(
    #         400, AppErrorCode.ERROR_DB_VALIDATION_ERROR, details=details
    #     )

    @app.errorhandler(UnprocessableEntity)
    def handle_unprocessable_entity(e):
        return _serialize_app_error(422, AppErrorCode.ERROR_UNPROCESSABLE)

    @app.errorhandler(HTTPException)
    def handle_application_http_error(e):
        http_error_code = e.code or 500
        app_error_code = AppErrorCode.ERROR_GENERIC.value.code
        msg = _translate(e.description)
        details = None

        if isinstance(e, ApplicationException):
            app_error_code = e.app_error_code
            details = e.detail

        return _serialize_error(http_error_code, app_error_code, msg, details)

    @app.errorhandler(Exception)
    def handle_unknown_exception(e):
        # XXX Conforme o caso, além de logar precisaríamos tratar?
        meta = {"error_key": uuid4()}
        logger.error("Erro inesperado na aplicacao", meta=meta)
        return _serialize_error(
            500,
            AppErrorCode.ERROR_GENERIC.value.code,
            "Erro inesperado",
            details=meta,
        )
