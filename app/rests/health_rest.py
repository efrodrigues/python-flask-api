from flask_smorest import Blueprint

from ..businesses.health_bo import ping_db
from ..configs.cache_config import cache
from ..utils.settings import get_app_version
from .schemas.health_schema import PingResponse

api = Blueprint(
    "Saúde",
    "health_rest",
    url_prefix="/api/health",
    description="Saúde da aplicação.",
)


@api.route("", methods=["GET"])
@api.response(
    PingResponse,
    description="""Sucesso de resposta da aplicação.

No caso de resposta de sucesso da aplicação, você receberá
 a seguinte informação:

- `pong`: Valor boleano informando o caso de sucesso. Sempre vem `true`.
- `version`: A versão da API.
""",
)
@cache.cached(timeout=30)
def ping():
    """
    "Saúde" da aplicação.

    Com esta chamada de _ping_ você
    você estará verificando:

    - Se a aplicação está respondendo/viva.
    - Batendo no banco de dados.
    """
    ping_db()
    return {"pong": True, "version": get_app_version()}


@api.route("/version", methods=["GET"])
@api.response(
    code=200, description="String com a versão da aplicação",
)
@cache.cached(timeout=30)
def get_version():
    """
    Versão da API.
    """
    return get_app_version()
