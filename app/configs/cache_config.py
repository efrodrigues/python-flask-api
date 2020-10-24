from flask import Flask
from flask_caching import Cache

# TODO: Revisar cache (sera necessario?)
cache = Cache(config={"CACHE_TYPE": "simple"})


def cache_config(app: Flask):
    cache.init_app(app)
