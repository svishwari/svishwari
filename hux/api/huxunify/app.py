"""
Purpose of this file is to house the main application code.
"""
import logging

from flask import Flask, request
from flasgger import Swagger
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from huxunify.api.config import load_env_vars
from huxunify.api.route import ROUTES
from huxunify.api import constants
from huxunify.api.route.utils import get_health_check


# set config variables
SWAGGER_CONFIG = {
    "uiversion": "3",
    "static_url_path": "/swagger",
    "title": "Hux API",
    "version": "1.0.0",
    "swagger_ui": True,
    "specs_route": "/api/v1/ui/",
    "description": "",
    "termsOfService": "",
    "schemes": ["https"],
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}


def configure_flask(flask_app: Flask) -> None:
    """Set configuration and variables for Flask.

    Args:
        flask_app (Flask): Flask application.

    Returns:

    """
    # setup the environment config
    try:
        if flask_app.config["ENV"] == constants.PRODUCTION_MODE:
            flask_app.config.from_object(
                "huxunify.api.config.ProductionConfig"
            )
        elif flask_app.config["ENV"] == constants.DEVELOPMENT_MODE:
            flask_app.config.from_object(
                "huxunify.api.config.DevelopmentConfig"
            )
        else:
            # use http by default for local testing.
            SWAGGER_CONFIG["schemes"].insert(0, "http")
            flask_app.config.from_object("huxunify.api.config.Config")
    except KeyError as error:
        desc = f"Environment not configured: {error} is required."
        raise Exception(desc) from error


def monitor_app(flask_app: Flask) -> None:
    """sets up prometheus monitoring for flask app

    Args:
        flask_app (Flask): Flask application.

    Returns:
        None

    """

    metrics = PrometheusMetrics(
        app=flask_app, defaults_prefix="/api/v1", export_defaults=False
    )

    metrics.register_default(
        metrics.counter(
            name="by_path_counter",
            description="Request count by request paths",
            labels={"path": lambda: request.path},
        )
    )

    metrics.register_default(
        metrics.histogram(
            name="requests_by_status_and_path",
            description="Response time by status and path",
            labels={"status": lambda r: r.status_code, "path": lambda: request.path},
            buckets=(.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0)
        )
    )


def create_app() -> Flask:
    """creates the flask app and blueprints

    Args:

    Returns:
        Flask: Returns a flask object.

    """
    load_env_vars()

    # setup the flask app
    flask_app = Flask(__name__)

    # setup CORS
    CORS(flask_app)

    # register the routes
    for route in ROUTES:
        logging.debug("Registering %s.", route.name)
        flask_app.register_blueprint(route, url_prefix="/api/v1")

    # add health check URLs
    # pylint: disable=unnecessary-lambda
    flask_app.add_url_rule(
        constants.HEALTH_CHECK_ENDPOINT,
        constants.HEALTH_CHECK,
        view_func=lambda: get_health_check().run(),
    )

    # setup the swagger docs
    Swagger(flask_app, config=SWAGGER_CONFIG, merge=True)

    # configure flask
    configure_flask(flask_app)

    # monitor flask setup
    # monitor_app(flask_app)

    return flask_app


# pylint: disable=no-member
if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    args = parser.parse_args()
    port = args.port

    # create the API
    app = create_app()

    # run the API
    app.run(host="0.0.0.0", port=port, debug=True)
