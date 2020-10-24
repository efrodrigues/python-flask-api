from maaslogger.base_logger import get_logger
from maaslogger.config import init_logger_config

from app import create_app
from app.utils import settings


def init_app():
    settings.load_settings()
    init_logger_config()
    return create_app()


app = init_app()

if __name__ == "__main__":
    get_logger(__name__).notice(f"Aplicacao iniciada na (porta_http={settings.get_app_port()})")
    app.run(host="0.0.0.0", port=settings.get_app_port())
