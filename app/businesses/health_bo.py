from maaslogger.base_logger import (
    LogLevel,
    LogTimeMessageConf,
    LogTimeMessageConfSource,
)
from maaslogger.rest_logger import get_logger

from ..configs.db_config import get_connection
from ..utils.db_util import find_sql_server_version
from ..utils.exceptions import AppErrorCode, ApplicationException

logger = get_logger(__name__)


@logger.time(
    info_msg=LogTimeMessageConf(
        severity=LogLevel.DEBUG,
        source=LogTimeMessageConfSource.FUNCTION_RETURN,
    ),
    err_msg="Falha no ping do bd",
)
def ping_db():
    try:
        db_version = find_sql_server_version(get_connection())
        return f"Conectado no banco Azure SQL (versao={db_version})"
    except Exception:
        raise ApplicationException(AppErrorCode.ERROR_DB_FAILED_PING)
