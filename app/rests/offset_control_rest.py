from flask_smorest import Blueprint
from maaslogger.rest_logger import get_logger

logger = get_logger(__name__)


api = Blueprint(
    "OffsetControl",
    "offset_control_rest",
    url_prefix="/api/offset-control",
    description="Controle de Offset",
)


@api.route("", methods=["GET"])
@api.response(
    code=200, description="""Obtem offset para realizar consulta""",
)
def get_offset_control():
    """
    Obtenção de offset para realização de consulta.
    """
    return 1
