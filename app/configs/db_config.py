import urllib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

from ..utils import settings

db = SQLAlchemy()


def db_config(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = get_app_db_uri()
    db.init_app(app)


def get_app_db_uri():
    user_database = settings.get_user_database()
    password_database = settings.get_password_database()
    url_database = settings.get_url_database()
    port_database = settings.get_port_database()
    database = settings.get_app_database()
    driver_odbc = settings.get_app_driver_odbc()

    """
    URI de conexão do banco de dados."
    """
    odbc_str = (
        f"DRIVER={driver_odbc};SERVER={url_database};PORT={port_database};"
        f"UID={user_database};DATABASE={database};PWD={password_database}"
    )
    connect_str = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(
        odbc_str
    )
    return connect_str


def get_db():
    return db


def get_session():
    return sessionmaker(bind=get_db())


def get_connection():
    return get_db().get_engine().connect()
