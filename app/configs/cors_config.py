from flask_cors import CORS


def cors_config(app):
    # TODO: Revisar CORS
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})
