from flask import Flask
from flasgger import Swagger
from shorten_url.controller.v1 import api_bp as api_bp_v1
from shorten_url.controller.v2 import api_bp as api_bp_v2
from shorten_url.variables import AppVars


def register_blueprint(app):
    app.register_blueprint(api_bp_v1, url_prefix="/shorten_url/v1")
    app.register_blueprint(api_bp_v2, url_prefix="/shorten_url/v2")


def setup_swagger(app):
    # https://github.com/flasgger/flasgger
    # http://localhost:8080/apidocs/
    if not AppVars.ENABLE_SWAGGER:
        return

    config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }
    Swagger(app, config=config)


def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    setup_swagger(app)
    return app


if __name__ == "__main__":
    pass
