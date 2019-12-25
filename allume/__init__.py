from flask import Flask
from config import get_config
from allume.core.db import DBAPI
from allume.apis.order_api import order_api_bp
# from .middleware import control

# def register_middleware(app):
#     app.register_blueprint(control)


def register_blueprints(app):
    app.register_blueprint(order_api_bp)


def create_app(env):
    app = Flask(__name__)

    config = get_config(env)
    app.config.from_object(config)
    DBAPI.init(config.DB_URI, config.DB_MAX_POOL_SIZE)
    
    # # register_middleware(app)
    register_blueprints(app)
    return app


