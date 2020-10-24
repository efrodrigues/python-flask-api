from dataclasses import dataclass
from enum import Enum

from werkzeug.exceptions import HTTPException


@dataclass
class InfoAppErrorCode(object):
    # Código de erro.
    code: int = 0
    # Descrição do erro.
    description: str = None


class AppErrorCode(Enum):
    """Códigos de erros da aplicação."""

    ERROR_NONE = InfoAppErrorCode(0, "Nenhum erro")

    # ============================================================
    # Erros gerais "internos" para os middlewares (Família 01-100)
    # ============================================================
    ERROR_GENERIC = InfoAppErrorCode(1, "Erro geral")
    ERROR_UNAUTHORIZED = InfoAppErrorCode(2, "Não autorizado")
    ERROR_FORBIDDEN = InfoAppErrorCode(3, "Acesso negado")
    ERROR_UNPROCESSABLE = InfoAppErrorCode(
        4, "Há campo(s) incorreto(s) ou faltando na requisição"
    )
    ERROR_COOKIE_NO_DOT = InfoAppErrorCode(5, "Cookie inválido.")
    ERROR_COOKIE_HASH = InfoAppErrorCode(6, "Cookie inválido.")

    # ============================================================
    # Erros para banco de dados (Família 100-200)
    # ============================================================
    ERROR_DB_FAILED_PING = InfoAppErrorCode(101, "Falha testar conexão banco")
    ERROR_DB_NOT_UNIQUE = InfoAppErrorCode(102, "Campo já existe")
    ERROR_DB_VALIDATION_ERROR = InfoAppErrorCode(
        103, "Falha na validação de um mais campos"
    )
    ERROR_DB_NOTFOUND_INVALID_OBJECT_ID = InfoAppErrorCode(
        103, "Registro não encontrado"
    )


class ApplicationException(HTTPException):
    def __init__(
        self,
        app_error_code: any,
        msg: str = None,
        detail: any = None,
        http_error_code: int = None,
    ):
        """
        Construtor.

        - app_error_code: Código do erro da aplicação. Ou pode ser uma
        instância de `AppErrorCode` ou um valor inteiro.
        - msg: Mensagem do erro. SE não for informado e `app_error_code`
        for uma instância de `AppErrorCode` então a sua mensagem será
        utilizada.
        - detail: Detalhe do erro.
        - http_error_code: Código do erro HTTP (valor padrão 500).
        """
        err_code, err_msg = self._read_error_code_msg(app_error_code, msg)
        self.app_error_code = err_code
        self.description = err_msg
        self.detail = detail
        self.code = http_error_code if http_error_code is not None else 500

    @staticmethod
    def _read_error_code_msg(app_error_code, msg):
        err_code = app_error_code
        err_msg = msg
        if isinstance(app_error_code, AppErrorCode):
            app_error_code = app_error_code.value
            err_code = app_error_code.code
            if err_msg is None:
                err_msg = app_error_code.description
        if err_msg is None:
            err_msg = "Erro interno no servidor"
        return err_code, err_msg


class UnauthorizedException(ApplicationException):
    def __init__(
        self, app_error_code: any = None, msg: str = None, detail: any = None,
    ):
        super(UnauthorizedException, self).__init__(
            (
                app_error_code
                if app_error_code is not None
                else AppErrorCode.ERROR_UNAUTHORIZED
            ),
            msg,
            detail,
            401,
        )


class ForbiddenException(ApplicationException):
    def __init__(
        self, app_error_code: any = None, msg: str = None, detail: any = None,
    ):
        super(ForbiddenException, self).__init__(
            (
                app_error_code
                if app_error_code is not None
                else AppErrorCode.ERROR_FORBIDDEN
            ),
            msg,
            detail,
            403,
        )


class ConflictException(ApplicationException):
    def __init__(
        self, app_error_code: any, msg: str = None, detail: any = None,
    ):
        super(ConflictException, self).__init__(
            app_error_code, msg, detail, 409
        )


class NotFoundException(ApplicationException):
    def __init__(
        self, app_error_code, msg: str = None, detail: any = None,
    ):
        super(NotFoundException, self).__init__(
            app_error_code, msg, detail, 404
        )


class RequestTimeout(ApplicationException):
    def __init__(
        self, app_error_code, msg: str = None, detail: any = None,
    ):
        super(RequestTimeout, self).__init__(app_error_code, msg, detail, 408)


class UnprocessableEntity(ApplicationException):
    def __init__(
        self, app_error_code, msg: str = None, detail: any = None,
    ):
        super(UnprocessableEntity, self).__init__(
            app_error_code, msg, detail, 422
        )
