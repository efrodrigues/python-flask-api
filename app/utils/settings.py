import os

import dotenv

from ..utils.constants import APP_VERSION


def load_settings():
    dotenv.load_dotenv()


def getenv(key, default=None) -> str:
    """
    Lê variável de ambiente.

    - key: str Chave.
    - default: Valor padrão para chave.

    Retorna:
    - str: Valor obtido ou o padrão.
    """
    return os.getenv(key, default)


def getenv_int(key, default=None) -> int:
    """
    Lê variável ambiente como valor inteiro.
    """
    value = getenv(key, default)
    if value is not None:
        value = int(value)
    return value


def get_app_port() -> int:
    """
    Porta de escuta da aplição.
    """
    return getenv_int("APP_PORT", 5000)


def get_app_version():
    """Versão da aplicação."""
    return getenv("APP_VERSION", APP_VERSION)


def get_user_database():
    """"Usuário do Banco de Dados"""
    return getenv("APP_USER_DATABASE")


def get_password_database():
    """"Senha do Banco de Dados"""
    return getenv("APP_PASSWORD_DATABASE")


def get_url_database():
    """"URL do Banco de Dados"""
    return getenv("APP_URL_DATABASE")


def get_port_database():
    """"Porta do Banco de Dados"""
    return getenv("APP_PORT_DATABASE")


def get_app_database():
    """"Nome do Banco de Dados"""
    return getenv("APP_DB_DATABASE")


def get_app_driver_odbc():
    """"Driver de conexão ao Banco de Dados"""
    return getenv("APP_DRIVER_ODBC")
