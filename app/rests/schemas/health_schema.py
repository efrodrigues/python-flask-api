from flask_marshmallow import Schema
from marshmallow import fields


class PingResponse(Schema):
    """Resposta ao ping da aplicação"""

    pong = fields.Boolean(required=True, description="Resposta do ping")
    version = fields.String(required=True, description="Versão da aplicação")
